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

# Register your models here.
