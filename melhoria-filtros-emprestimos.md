# Melhoria — Adicionar Filtros na Tela de Empréstimos

Este guia adiciona filtros à tela de **Empréstimos** da Mini Biblioteca Virtual, permitindo buscar por **livro**, **leitor** e **status** (ativo/finalizado) usando a biblioteca `django-filter`.

---

## 1) Objetivo

Permitir que o usuário filtre os empréstimos com base em critérios específicos diretamente na interface.

Exemplo: listar apenas os empréstimos de um determinado leitor, ou somente os que ainda não foram devolvidos.

---

## 2) Instalar o `django-filter` (caso ainda não tenha)

```bash
pip install django-filter
```

Em seguida, adicione no `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'django_filters',
]
```

---

## 3) Criar o arquivo `biblioteca/filters.py`

Crie o arquivo e adicione o seguinte conteúdo:

```python
import django_filters
from .models import Emprestimo

class EmprestimoFilter(django_filters.FilterSet):
    class Meta:
        model = Emprestimo
        fields = {
            'livro__titulo': ['icontains'],
            'leitor__nome': ['icontains'],
            'data_devolucao': ['lte', 'gte'],
        }
```

Isso cria filtros automáticos por **título do livro**, **nome do leitor** e **intervalo de data de devolução**.

---

## 4) Atualizar a view `emprestimos` em `biblioteca/views.py`

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Emprestimo
from .filters import EmprestimoFilter

@login_required
def emprestimos(request):
    emprestimos = Emprestimo.objects.select_related('livro', 'leitor').all()
    filtro = EmprestimoFilter(request.GET, queryset=emprestimos)
    emprestimos_filtrados = filtro.qs

    return render(request, 'emprestimos.html', {
        'filtro': filtro,
        'emprestimos': emprestimos_filtrados
    })
```

---

## 5) Alterar o Template `templates/emprestimos.html`

Logo acima da tabela de empréstimos, adicione o formulário de filtros.

```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="container mt-4">
  <h2>📖 Lista de Empréstimos</h2>
  <hr>

  <!-- Formulário de Filtro -->
  <form method="get" class="row g-2 mb-3">
    <div class="col-md-4 col-12">
      <input type="text" name="livro__titulo__icontains" class="form-control" placeholder="Buscar por título" value="{{ request.GET.livro__titulo__icontains }}">
    </div>
    <div class="col-md-4 col-12">
      <input type="text" name="leitor__nome__icontains" class="form-control" placeholder="Buscar por leitor" value="{{ request.GET.leitor__nome__icontains }}">
    </div>
    <div class="col-md-2 col-6">
      <input type="date" name="data_devolucao__gte" class="form-control" value="{{ request.GET.data_devolucao__gte }}">
    </div>
    <div class="col-md-2 col-6">
      <input type="date" name="data_devolucao__lte" class="form-control" value="{{ request.GET.data_devolucao__lte }}">
    </div>
    <div class="col-12 mt-2">
      <button type="submit" class="btn btn-primary w-100">Filtrar</button>
    </div>
  </form>

  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <th>Livro</th>
        <th>Leitor</th>
        <th>Data de Empréstimo</th>
        <th>Data de Devolução</th>
      </tr>
    </thead>
    <tbody>
      {% for e in emprestimos %}
      <tr>
        <td>{{ e.livro.titulo }}</td>
        <td>{{ e.leitor.nome }}</td>
        <td>{{ e.data_emprestimo }}</td>
        <td>{{ e.data_devolucao|default:"-" }}</td>
      </tr>
      {% empty %}
      <tr>
        <td colspan="4" class="text-center text-muted">Nenhum empréstimo encontrado.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
```

---

## 6) Testar a funcionalidade

1. Acesse `/emprestimos/`
2. Use os campos de busca para filtrar por **livro**, **leitor** ou **data de devolução**
3. Verifique que os resultados atualizam automaticamente após enviar o formulário.

---

## 7) Resumo da Melhoria

✅ Filtro por título do livro, nome do leitor e data de devolução  
✅ Implementação simples com `django-filter`  
✅ Interface responsiva e integrada ao Bootstrap  
✅ Funciona sem alterar o modelo existente
