from django.shortcuts import render, get_object_or_404

from .models import Receita

def lista_receitas(request):
    """Exibe todas as receitas publicadas, das mais recentes"""
    receitas = Receita.objects.filter(publicada=True)
    context = {
        "receitas": receitas,
    }
    return render(request, "receitas/lista.html", context)

def exibir_receita(request, pk):

    receita = get_object_or_404(
        Receita,
        pk=pk,
        publicada=True,
    )

    context = {
        'receita': receita,
    }

    return render(request, "receitas/exibir_receita.html", context)  