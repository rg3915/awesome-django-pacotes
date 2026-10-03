from django.shortcuts import render

from .models import Livro


def relatorio_n_mais_1(request):
    """De propósito: 1 query para os livros + 1 query por categoria (N+1)."""
    livros = Livro.objects.all()
    return render(request, "loja/relatorio.html", {"livros": livros, "titulo": "Relatório (N+1)"})


def relatorio_otimizado(request):
    """Mesmo relatório com select_related: 1 query só."""
    livros = Livro.objects.select_related("categoria")
    return render(request, "loja/relatorio.html", {"livros": livros, "titulo": "Relatório otimizado"})
