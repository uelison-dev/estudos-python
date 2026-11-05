#=====================
# paginas - views.py
#=====================

from django.shortcuts import render

# home () - retorna a página estática paginas/index.html
def home (request):
    return render (
        request,
        'paginas/home.html',
        { 'titulo': "Página Principal" }
    )

# sobre () - retorna a página estática paginas/sobre.html
def sobre(request):
    return render(
        request,
        "paginas/sobre.html",
        {"titulo": "Sobre Nós"},
    )

# contato () - retorna a página estática paginas/contato.html
def contato(request):
    return render(
        request,
        "paginas/contato.html",
        {"titulo": "Contato"},
    )

# politica_privacidade () - retorna a página estática paginas/politica_privacidade.html
def politica_privacidade(request):
    return render(
        request,
        "paginas/politica_privacidade.html",
        {"titulo": "Política de Privacidade"},
    )

