from rest_framework import viewsets

from .filters import LivroFilter
from .models import Livro
from .serializers import LivroSerializer


class LivroViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Livro.objects.select_related("categoria")
    serializer_class = LivroSerializer
    filterset_class = LivroFilter  # django-filter
