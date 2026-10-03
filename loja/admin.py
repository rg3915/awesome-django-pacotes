from django.conf import settings
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Categoria, Livro
from .resources import LivroResource

if settings.USE_UNFOLD:
    from unfold.admin import ModelAdmin
    from unfold.contrib.import_export.forms import ExportForm, ImportForm
else:  # admin padrão do Django, para comparação antes/depois
    from django.contrib.admin import ModelAdmin

    ExportForm = ImportForm = None


@admin.register(Categoria)
class CategoriaAdmin(ModelAdmin):
    list_display = ["nome", "slug"]
    prepopulated_fields = {"slug": ["nome"]}


@admin.register(Livro)
class LivroAdmin(SimpleHistoryAdmin, ImportExportModelAdmin, ModelAdmin):
    resource_classes = [LivroResource]
    list_display = ["titulo", "autor", "categoria", "preco", "estoque", "publicado_em"]
    list_filter = ["categoria", "publicado_em"]
    search_fields = ["titulo", "autor"]
    history_list_display = ["preco", "estoque"]
    list_filter_sheet = False  # unfold: filtros na lateral

    if ImportForm:
        import_form_class = ImportForm
        export_form_class = ExportForm
