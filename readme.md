# Mini Biblioteca Virtual

Projeto web em Django para gerenciar livros, leitores e empréstimos, com autenticação por sessão, templates Bootstrap e filtros usando `django-filter`.

## Requisitos
- `Python` 3.10 ou superior (recomendado 3.11/3.12)
- `pip` atualizado
- Opcional: `virtualenv` para ambiente isolado

## Tecnologias
- Django (5.x)
- django-filter
- Templates Django (sem React)
- Bootstrap 5 (via CDN)
- JavaScript puro
- Banco SQLite3 (padrão)

## Estrutura
- Projeto: `core`
- App principal: `biblioteca`
- Templates: `templates/`
- Banco: `db.sqlite3`
- Idioma: `pt-br`
- Fuso horário: `America/Sao_Paulo`

## Instalação
1. (Opcional) Crie e ative um ambiente virtual:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
2. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```

## Banco de Dados
1. Gere e aplique migrações:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Crie um superusuário para acesso:
   ```powershell
   python manage.py createsuperuser
   ```

## Executar o Servidor
```powershell
python manage.py runserver
```
Acesse: `http://127.0.0.1:8000/`

## Autenticação
- Login: `http://127.0.0.1:8000/login/`
- Logout: `http://127.0.0.1:8000/logout/`
- Todas as páginas internas exigem login.

## URLs Principais
- `/` → Página inicial (resumo do sistema)
- `/livros/` → Listar livros (com filtros por título, autor, disponibilidade)
- `/livros/novo/` → Cadastrar livro
- `/livros/<id>/editar/` → Editar livro
- `/livros/<id>/excluir/` → Excluir livro
- `/leitores/` → Listar leitores
- `/leitores/novo/` → Cadastrar leitor
- `/leitores/<id>/editar/` → Editar leitor
- `/leitores/<id>/excluir/` → Excluir leitor
- `/emprestimos/` → Listar empréstimos
- `/emprestimos/novo/` → Registrar empréstimo
- `/emprestimos/<id>/devolver/` → Marcar devolução
- `/admin/` → Admin Django

## Regras de Negócio
- Empréstimos:
  - Impede empréstimo se `livro.disponivel == False`.
  - Ao emprestar: marca `livro.disponivel = False`.
  - Ao devolver: define `data_devolucao` e marca `livro.disponivel = True`.

## Interface
- Bootstrap 5 por CDN em `templates/base.html`.
- Navbar e mensagens (`django.contrib.messages`).
- Função JS: `confirmarAcao(msg)` para confirmar exclusões e devoluções.
- Menu visível apenas quando autenticado.

## Dicas e Problemas Comuns
- Se a página de login não carregar, confirme em `core/settings.py`:
  - `INSTALLED_APPS` contém `'biblioteca'` e `'django_filters'`.
  - `TEMPLATES['DIRS'] = [BASE_DIR / 'templates']`.
  - `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` definidos.
- Certifique-se de que as migrações foram criadas e aplicadas.
- Use o admin (`/admin/`) para verificar e editar dados rapidamente.

## Licença
Uso educacional/demonstração.