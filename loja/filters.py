import django_filters

from .models import Livro


class LivroFilter(django_filters.FilterSet):
    categoria = django_filters.CharFilter(field_name="categoria__slug", label="Categoria (slug)")

    class Meta:
        model = Livro
        fields = {
            "preco": ["gt", "lt"],
            "publicado_em": ["year"],
            "autor": ["icontains"],
        }
