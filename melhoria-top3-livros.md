# Melhoria — Exibir Top 3 Livros Mais Emprestados na Home

Passo a passo para adicionar ao projeto da Mini Biblioteca Virtual um painel na tela inicial (`home.html`) mostrando os **3 livros mais emprestados**.

---

## 1) Objetivo

Exibir, logo abaixo do resumo de contagens, uma seção com os **Top 3 livros mais emprestados**, baseando-se na quantidade de registros de empréstimos (`Emprestimo`) relacionados a cada livro.

---

## 2) Ajuste em `biblioteca/views.py`

Adicione a importação do `Count` e ajuste a função `home`:

```python
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Livro, Leitor, Emprestimo

@login_required
def home(request):
    contagem = {
        "livros": Livro.objects.count(),
        "leitores": Leitor.objects.count(),
        "emprestimos": Emprestimo.objects.count(),
    }

    # Top 3 livros mais emprestados
    top_livros = (
        Livro.objects.annotate(total_emprestimos=Count("emprestimo"))
        .order_by("-total_emprestimos")[:3]
    )

    return render(
        request,
        "home.html",
        {"contagem": contagem, "top_livros": top_livros},
    )
```

---

## 3) Atualizar o Template `templates/home.html`

Abaixo das cards de contagem, adicione a nova seção **Top 3 Livros Mais Emprestados**.

```html
{% extends 'base.html' %}
{% block content %}
<div class="row">
  <div class="col-12 mb-4">
    <h1>Bem-vindo à Mini Biblioteca Virtual</h1>
    <p class="text-muted">Resumo do sistema</p>
  </div>

  <!-- Cards de contagem -->
  <div class="col-md-4">
    <div class="card mb-3">
      <div class="card-body text-center">
        <h5 class="card-title">Livros</h5>
        <p class="card-text display-6">{{ contagem.livros }}</p>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card mb-3">
      <div class="card-body text-center">
        <h5 class="card-title">Leitores</h5>
        <p class="card-text display-6">{{ contagem.leitores }}</p>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card mb-3">
      <div class="card-body text-center">
        <h5 class="card-title">Empréstimos</h5>
        <p class="card-text display-6">{{ contagem.emprestimos }}</p>
      </div>
    </div>
  </div>
</div>

<hr>

<!-- NOVA SEÇÃO: Top 3 Livros Mais Emprestados -->
<div class="row mt-4">
  <div class="col-12">
    <h3>📚 Top 3 Livros Mais Emprestados</h3>
  </div>

  {% if top_livros %}
    {% for livro in top_livros %}
    <div class="col-md-4 col-12">
      <div class="card mb-3 shadow-sm">
        <div class="card-body text-center">
          <h5 class="card-title">{{ livro.titulo }}</h5>
          <p class="card-text text-muted mb-1">{{ livro.autor }}</p>
          <p class="fw-bold mb-0">{{ livro.total_emprestimos }} empréstimos</p>
        </div>
      </div>
    </div>
    {% endfor %}
  {% else %}
    <p class="text-muted">Nenhum empréstimo registrado ainda.</p>
  {% endif %}
</div>
{% endblock %}
```

---

## 4) Testar no navegador

1. Execute o servidor:
   ```powershell
   python manage.py runserver
   ```
2. Acesse:  
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

3. Na tela inicial, logo abaixo do resumo, será exibida uma seção mostrando os **3 livros mais emprestados**, atualizada dinamicamente conforme novos empréstimos forem registrados.

---

## 5) Resumo da Melhoria

✅ Exibe os 3 livros mais emprestados  
✅ Atualiza automaticamente conforme novos empréstimos  
✅ Não requer novo modelo nem campo adicional  
✅ Mantém o padrão de estilo e layout Bootstrap do projeto
