from rest_framework import serializers

from .models import Livro


class LivroSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField()

    class Meta:
        model = Livro
        fields = ["id", "titulo", "autor", "preco", "categoria", "publicado_em", "estoque"]
