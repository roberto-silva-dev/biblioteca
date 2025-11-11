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