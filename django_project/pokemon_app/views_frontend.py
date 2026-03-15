from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def index_page(request):
    """Renders the index.html page."""
    return render(request, 'index.html')


def login_page(request):
    """Renders login page that authenticates via API call."""
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'login.html')


def register_page(request):
    """Renders register page that creates users via API call."""
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'register.html')


def pokemon_page(request):
    """Renders the pokemon.html page."""
    return render(request, 'pokemon.html')


@login_required
def create_team_page(request):
    """Renders the create_team.html page."""
    return render(request, 'create_team.html', {'slots': range(1, 7)})


@login_required
def teams_page(request):
    """Renders the teams.html page."""
    return render(request, 'teams.html')


@login_required
def edit_team_page(request, team_id):
    """Renders the edit_team.html page."""
    return render(request, 'edit_team.html', {'team_id': team_id, 'slots': range(1, 7)})


def analysis_page(request, team_id):
    """Renders the analysis.html page."""
    return render(request, 'analysis.html', {'team_id': team_id})


def global_stats_page(request):
    """Renders the global_stats.html page."""
    return render(request, 'global_stats.html')
