from django.urls import path
from pokemon_app.views_api import (
    login_api,
    register_api,
    pokemon_api,
    team_detail_api,
    team_analysis_api,
    teams_api,
    top_pokemon_usage_api,
    top_type_usage_api,
)

urlpatterns = [
    path('auth/users/', register_api, name='register_api'),
    path('auth/sessions/', login_api, name='login_api'),
    path('pokemon/', pokemon_api, name='pokemon_api'),
    path('teams/', teams_api, name='teams_api'),
    path('teams/<int:team_id>/', team_detail_api, name='team_detail_api'),
    path('teams/<int:team_id>/analysis/', team_analysis_api, name='team_analysis_api'),
    path('stats/top-pokemon/', top_pokemon_usage_api, name='top_pokemon_usage_api'),
    path('stats/top-types/', top_type_usage_api, name='top_type_usage_api'),
]
