from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import Categoria, Livro


class LivroResource(resources.ModelResource):
    categoria = fields.Field(
        column_name="categoria",
        attribute="categoria",
        widget=ForeignKeyWidget(Categoria, field="nome"),
    )

    class Meta:
        model = Livro
        fields = ("id", "titulo", "autor", "preco", "categoria", "publicado_em", "estoque")
        export_order = fields
