# Criando do Zero — Mini Biblioteca Virtual (Django)

Passo a passo para criar o projeto do zero, com o projeto `core` e o app `biblioteca`, incluindo os arquivos e códigos necessários.

## 1) Criar projeto e app
1. Verifique a versão do Django:
   ```powershell
   python -m django --version
   ```
2. Crie o projeto `core` na raiz atual:
   ```powershell
   django-admin startproject core .
   ```
3. Crie o app `biblioteca`:
   ```powershell
   python manage.py startapp biblioteca
   ```

## 2) Dependências
1. Crie `requirements.txt` na raiz com:
   ```text
   Django>=5.2,<6.0
   django-filter>=24.2
   ```
2. Instale:
   ```powershell
   pip install -r requirements.txt
   ```

## 3) Configurar `core/settings.py`
- Abra `core/settings.py` e ajuste:

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',      # terceiro
    'biblioteca',          # app do projeto
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Idioma e fuso horário
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

# Arquivos estáticos
STATIC_URL = 'static/'

# Redirects de autenticação
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
```

## 4) Configurar `core/urls.py`
Crie/edite `core/urls.py` para incluir as rotas de login/logout e as URLs do app:

```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticação padrão
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # App
    path('', include('biblioteca.urls')),
]
```

## 5) Modelos — `biblioteca/models.py`
Crie os modelos conforme as regras do sistema:

```python
from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    ano_publicacao = models.IntegerField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} ({self.autor})"

class Leitor(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    leitor = models.ForeignKey(Leitor, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.livro.titulo} - {self.leitor.nome}"
```

## 6) Forms — `biblioteca/forms.py`

```python
from django import forms
from .models import Livro, Leitor, Emprestimo

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ["titulo", "autor", "ano_publicacao", "disponivel"]

class LeitorForm(forms.ModelForm):
    class Meta:
        model = Leitor
        fields = ["nome", "email"]

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ["livro", "leitor"]

    def clean(self):
        cleaned_data = super().clean()
        livro = cleaned_data.get("livro")
        if livro and not livro.disponivel:
            raise forms.ValidationError("Este livro não está disponível para empréstimo.")
        return cleaned_data
```

## 7) Filtros — `biblioteca/filters.py`

```python
import django_filters
from .models import Livro

class LivroFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(field_name="titulo", lookup_expr="icontains", label="Título")
    autor = django_filters.CharFilter(field_name="autor", lookup_expr="icontains", label="Autor")
    disponivel = django_filters.BooleanFilter(field_name="disponivel", label="Disponível")

    class Meta:
        model = Livro
        fields = ["titulo", "autor", "disponivel"]
```

## 8) Views — `biblioteca/views.py`

```python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .models import Livro, Leitor, Emprestimo
from .forms import LivroForm, LeitorForm, EmprestimoForm
from .filters import LivroFilter

@login_required
def home(request):
    contagem = {
        "livros": Livro.objects.count(),
        "leitores": Leitor.objects.count(),
        "emprestimos": Emprestimo.objects.count(),
    }
    return render(request, "home.html", {"contagem": contagem})

class LivroListView(LoginRequiredMixin, FilterView):
    model = Livro
    filterset_class = LivroFilter
    template_name = "livros/list.html"
    context_object_name = "livros"
    paginate_by = 20

class LivroCreateView(LoginRequiredMixin, CreateView):
    model = Livro
    form_class = LivroForm
    template_name = "livros/form.html"
    success_url = reverse_lazy("livro_list")
    def form_valid(self, form):
        messages.success(self.request, "Livro cadastrado com sucesso.")
        return super().form_valid(form)

class LivroUpdateView(LoginRequiredMixin, UpdateView):
    model = Livro
    form_class = LivroForm
    template_name = "livros/form.html"
    success_url = reverse_lazy("livro_list")
    def form_valid(self, form):
        messages.success(self.request, "Livro atualizado com sucesso.")
        return super().form_valid(form)

class LivroDeleteView(LoginRequiredMixin, DeleteView):
    model = Livro
    template_name = "livros/confirm_delete.html"
    success_url = reverse_lazy("livro_list")
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Livro excluído com sucesso.")
        return super().delete(request, *args, **kwargs)

class LeitorListView(LoginRequiredMixin, ListView):
    model = Leitor
    template_name = "leitores/list.html"
    context_object_name = "leitores"
    paginate_by = 20

class LeitorCreateView(LoginRequiredMixin, CreateView):
    model = Leitor
    form_class = LeitorForm
    template_name = "leitores/form.html"
    success_url = reverse_lazy("leitor_list")
    def form_valid(self, form):
        messages.success(self.request, "Leitor cadastrado com sucesso.")
        return super().form_valid(form)

class LeitorUpdateView(LoginRequiredMixin, UpdateView):
    model = Leitor
    form_class = LeitorForm
    template_name = "leitores/form.html"
    success_url = reverse_lazy("leitor_list")
    def form_valid(self, form):
        messages.success(self.request, "Leitor atualizado com sucesso.")
        return super().form_valid(form)

class LeitorDeleteView(LoginRequiredMixin, DeleteView):
    model = Leitor
    template_name = "leitores/confirm_delete.html"
    success_url = reverse_lazy("leitor_list")
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Leitor excluído com sucesso.")
        return super().delete(request, *args, **kwargs)

class EmprestimoListView(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = "emprestimos/list.html"
    context_object_name = "emprestimos"
    paginate_by = 20

class EmprestimoCreateView(LoginRequiredMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = "emprestimos/form.html"
    success_url = reverse_lazy("emprestimo_list")
    def form_valid(self, form):
        response = super().form_valid(form)
        emprestimo = self.object
        livro = emprestimo.livro
        if livro.disponivel:
            livro.disponivel = False
            livro.save()
            messages.success(self.request, "Empréstimo registrado com sucesso.")
        else:
            messages.error(self.request, "Este livro não está disponível.")
            return redirect("emprestimo_create")
        return response

@login_required
def devolver_emprestimo(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if emprestimo.data_devolucao:
        messages.info(request, "Este empréstimo já foi devolvido.")
    else:
        emprestimo.data_devolucao = timezone.now().date()
        emprestimo.save()
        livro = emprestimo.livro
        livro.disponivel = True
        livro.save()
        messages.success(request, "Devolução registrada com sucesso.")
    return redirect("emprestimo_list")
```

## 9) URLs do app — `biblioteca/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Livros
    path('livros/', views.LivroListView.as_view(), name='livro_list'),
    path('livros/novo/', views.LivroCreateView.as_view(), name='livro_create'),
    path('livros/<int:pk>/editar/', views.LivroUpdateView.as_view(), name='livro_update'),
    path('livros/<int:pk>/excluir/', views.LivroDeleteView.as_view(), name='livro_delete'),

    # Leitores
    path('leitores/', views.LeitorListView.as_view(), name='leitor_list'),
    path('leitores/novo/', views.LeitorCreateView.as_view(), name='leitor_create'),
    path('leitores/<int:pk>/editar/', views.LeitorUpdateView.as_view(), name='leitor_update'),
    path('leitores/<int:pk>/excluir/', views.LeitorDeleteView.as_view(), name='leitor_delete'),

    # Empréstimos
    path('emprestimos/', views.EmprestimoListView.as_view(), name='emprestimo_list'),
    path('emprestimos/novo/', views.EmprestimoCreateView.as_view(), name='emprestimo_create'),
    path('emprestimos/<int:pk>/devolver/', views.devolver_emprestimo, name='emprestimo_devolver'),
]
```

## 10) Admin — `biblioteca/admin.py`

```python
from django.contrib import admin
from .models import Livro, Leitor, Emprestimo

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "ano_publicacao", "disponivel")
    search_fields = ("titulo", "autor")
    list_filter = ("disponivel", "ano_publicacao")

@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = ("nome", "email")
    search_fields = ("nome", "email")

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ("livro", "leitor", "data_emprestimo", "data_devolucao")
    search_fields = ("livro__titulo", "leitor__nome")
    list_filter = ("data_devolucao",)
```

## 11) Templates — pasta `templates/`
Crie a estrutura de templates e os arquivos abaixo.

### `templates/base.html`
```html
<!doctype html>
<html lang="pt-br">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mini Biblioteca Virtual</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Biblioteca</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          {% if user.is_authenticated %}
          <ul class="navbar-nav me-auto">
            <li class="nav-item"><a class="nav-link" href="/">Início</a></li>
            <li class="nav-item"><a class="nav-link" href="/livros/">Livros</a></li>
            <li class="nav-item"><a class="nav-link" href="/leitores/">Leitores</a></li>
            <li class="nav-item"><a class="nav-link" href="/emprestimos/">Empréstimos</a></li>
          </ul>
          <ul class="navbar-nav">
            <form action="/logout/" method="post" style="display: inline;">
              {% csrf_token %}
              <button type="submit" class="btn nav-link" onclick="return confirmarAcao('Tem certeza que deseja sair?');">Sair</button>
            </form>
          </ul>
          {% endif %}
        </div>
      </div>
    </nav>

    <div class="container">
      {% if messages %}
        <div class="mt-2">
          {% for message in messages %}
            <div class="alert alert-{{ message.tags }}" role="alert">{{ message }}</div>
          {% endfor %}
        </div>
      {% endif %}

      {% block content %}{% endblock %}
    </div>

    <script>
      function confirmarAcao(msg) { return confirm(msg); }
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
```

### `templates/login.html`
```html
{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-md-4">
    <div class="card">
      <div class="card-header">Entrar</div>
      <div class="card-body">
        <form method="post">
          {% csrf_token %}
          {{ form.as_p }}
          <button type="submit" class="btn btn-primary w-100">Login</button>
        </form>
      </div>
    </div>
  </div>
  <div class="text-center mt-3 text-muted">Faça login para acessar o sistema.</div>
</div>
{% endblock %}
```

### `templates/home.html`
```html
{% extends 'base.html' %}
{% block content %}
<div class="row">
  <div class="col-12">
    <h1>Bem-vindo à Mini Biblioteca Virtual</h1>
    <p class="text-muted">Resumo do sistema</p>
  </div>
  <div class="col-md-4"><div class="card mb-3"><div class="card-body"><h5 class="card-title">Livros</h5><p class="card-text display-6">{{ contagem.livros }}</p></div></div></div>
  <div class="col-md-4"><div class="card mb-3"><div class="card-body"><h5 class="card-title">Leitores</h5><p class="card-text display-6">{{ contagem.leitores }}</p></div></div></div>
  <div class="col-md-4"><div class="card mb-3"><div class="card-body"><h5 class="card-title">Empréstimos</h5><p class="card-text display-6">{{ contagem.emprestimos }}</p></div></div></div>
</div>
{% endblock %}
```

### `templates/livros/list.html`
```html
{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h2>Livros</h2>
  <a href="/livros/novo/" class="btn btn-success">Novo Livro</a>
</div>

<form method="get" class="row g-2 mb-3">
  <div class="col-md-4">
    <label for="{{ filter.form.titulo.id_for_label }}" class="form-label">{{ filter.form.titulo.label }}</label>
    {{ filter.form.titulo }}
  </div>
  <div class="col-md-4">
    <label for="{{ filter.form.autor.id_for_label }}" class="form-label">{{ filter.form.autor.label }}</label>
    {{ filter.form.autor }}
  </div>
  <div class="col-md-2">
    <label for="{{ filter.form.disponivel.id_for_label }}" class="form-label">{{ filter.form.disponivel.label }}</label>
    {{ filter.form.disponivel }}
  </div>
  <div class="col-md-2 align-self-end">
    <button class="btn btn-primary w-100" type="submit">Filtrar</button>
  </div>
  <div class="col-12">
    <a href="/livros/" class="btn btn-link">Limpar filtros</a>
  </div>
  {{ filter.form.media }}
  </form>

<table class="table table-striped">
  <thead><tr><th>Título</th><th>Autor</th><th>Ano</th><th>Disponível</th><th class="text-end">Ações</th></tr></thead>
  <tbody>
    {% for livro in livros %}
    <tr>
      <td>{{ livro.titulo }}</td>
      <td>{{ livro.autor }}</td>
      <td>{{ livro.ano_publicacao }}</td>
      <td>{% if livro.disponivel %}<span class="badge text-bg-success">Sim</span>{% else %}<span class="badge text-bg-secondary">Não</span>{% endif %}</td>
      <td class="text-end">
        <a href="/livros/{{ livro.id }}/editar/" class="btn btn-sm btn-primary">Editar</a>
        <a href="/livros/{{ livro.id }}/excluir/" class="btn btn-sm btn-danger" onclick="return confirmarAcao('Deseja excluir este livro?');">Excluir</a>
      </td>
    </tr>
    {% empty %}
    <tr><td colspan="5" class="text-center">Nenhum livro encontrado.</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```

### `templates/livros/form.html`
```html
{% extends 'base.html' %}
{% block content %}
<h2>{% if object %}Editar Livro{% else %}Novo Livro{% endif %}</h2>
<form method="post" class="mt-3">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit" class="btn btn-primary">Salvar</button>
  <a href="/livros/" class="btn btn-secondary">Cancelar</a>
</form>
{% endblock %}
```

### `templates/livros/confirm_delete.html`
```html
{% extends 'base.html' %}
{% block content %}
<h2>Confirmar exclusão</h2>
<p>Tem certeza que deseja excluir "{{ object }}"?</p>
<form method="post" onsubmit="return confirmarAcao('Excluir definitivamente?');">
  {% csrf_token %}
  <button type="submit" class="btn btn-danger">Excluir</button>
  <a href="/livros/" class="btn btn-secondary">Cancelar</a>
</form>
{% endblock %}
```

### `templates/leitores/list.html`
```html
{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h2>Leitores</h2>
  <a href="/leitores/novo/" class="btn btn-success">Novo Leitor</a>
</div>

<table class="table table-striped">
  <thead><tr><th>Nome</th><th>Email</th><th class="text-end">Ações</th></tr></thead>
  <tbody>
    {% for leitor in leitores %}
    <tr>
      <td>{{ leitor.nome }}</td>
      <td>{{ leitor.email }}</td>
      <td class="text-end">
        <a href="/leitores/{{ leitor.id }}/editar/" class="btn btn-sm btn-primary">Editar</a>
        <a href="/leitores/{{ leitor.id }}/excluir/" class="btn btn-sm btn-danger" onclick="return confirmarAcao('Deseja excluir este leitor?');">Excluir</a>
      </td>
    </tr>
    {% empty %}
    <tr><td colspan="3" class="text-center">Nenhum leitor cadastrado.</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```

### `templates/leitores/form.html`
```html
{% extends 'base.html' %}
{% block content %}
<h2>{% if object %}Editar Leitor{% else %}Novo Leitor{% endif %}</h2>
<form method="post" class="mt-3">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit" class="btn btn-primary">Salvar</button>
  <a href="/leitores/" class="btn btn-secondary">Cancelar</a>
</form>
{% endblock %}
```

### `templates/leitores/confirm_delete.html`
```html
{% extends 'base.html' %}
{% block content %}
<h2>Confirmar exclusão</h2>
<p>Tem certeza que deseja excluir "{{ object }}"?</p>
<form method="post" onsubmit="return confirmarAcao('Excluir definitivamente?');">
  {% csrf_token %}
  <button type="submit" class="btn btn-danger">Excluir</button>
  <a href="/leitores/" class="btn btn-secondary">Cancelar</a>
</form>
{% endblock %}
```

### `templates/emprestimos/list.html`
```html
{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h2>Empréstimos</h2>
  <a href="/emprestimos/novo/" class="btn btn-success">Novo Empréstimo</a>
</div>

<table class="table table-striped">
  <thead>
    <tr>
      <th>Livro</th><th>Leitor</th><th>Data Empréstimo</th><th>Devolução</th><th class="text-end">Ações</th>
    </tr>
  </thead>
  <tbody>
    {% for emp in emprestimos %}
    <tr>
      <td>{{ emp.livro.titulo }}</td>
      <td>{{ emp.leitor.nome }}</td>
      <td>{{ emp.data_emprestimo }}</td>
      <td>{% if emp.data_devolucao %}{{ emp.data_devolucao }}{% else %}<span class="badge text-bg-warning">Em aberto</span>{% endif %}</td>
      <td class="text-end">
        {% if not emp.data_devolucao %}
        <a href="/emprestimos/{{ emp.id }}/devolver/" class="btn btn-sm btn-primary" onclick="return confirmarAcao('Confirmar devolução?');">Marcar devolução</a>
        {% endif %}
      </td>
    </tr>
    {% empty %}
    <tr><td colspan="5" class="text-center">Nenhum empréstimo encontrado.</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```

### `templates/emprestimos/form.html`
```html
{% extends 'base.html' %}
{% block content %}
<h2>Novo Empréstimo</h2>
<form method="post" class="mt-3">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit" class="btn btn-primary">Salvar</button>
  <a href="/emprestimos/" class="btn btn-secondary">Cancelar</a>
</form>
{% endblock %}
```

## 12) Migrações e superusuário
Gere e aplique migrações e crie um usuário administrador:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 13) Executar
Inicie o servidor de desenvolvimento:

```powershell
python manage.py runserver
```
Acesse `http://127.0.0.1:8000/login/` para entrar e navegar pelo sistema.

## 14) Regras de Negócio (resumo)
- Impede empréstimo se `livro.disponivel == False`.
- Ao emprestar: marca `livro.disponivel = False`.
- Ao devolver: define `data_devolucao` e marca `livro.disponivel = True`.

---