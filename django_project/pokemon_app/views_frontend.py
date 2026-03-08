from django.shortcuts import render


def pokemon_page(request):
    """Renders the pokemon.html page."""
    return render(request, 'pokemon.html')
