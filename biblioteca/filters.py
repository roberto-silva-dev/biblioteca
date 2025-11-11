import django_filters
from .models import Livro


class LivroFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(field_name="titulo", lookup_expr="icontains", label="Título")
    autor = django_filters.CharFilter(field_name="autor", lookup_expr="icontains", label="Autor")
    disponivel = django_filters.BooleanFilter(field_name="disponivel", label="Disponível")

    class Meta:
        model = Livro
        fields = ["titulo", "autor", "disponivel"]