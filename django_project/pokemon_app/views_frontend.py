from django.shortcuts import render


def index_page(request):
    """Renders the index.html page."""
    return render(request, 'index.html')


def pokemon_page(request):
    """Renders the pokemon.html page."""
    return render(request, 'pokemon.html')
