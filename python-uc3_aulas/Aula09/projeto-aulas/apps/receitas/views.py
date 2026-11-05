from django.shortcuts import render, get_object_or_404

from .models import Receita

def lista_receitas(request):
    """Exibe todas as receitas publicadas, das mais recentes"""
    receitas = Receita.objects.filter(publicada=True)
    context = {
        "receitas": receitas,
    }
    return render(request, "receitas/lista.html", context)