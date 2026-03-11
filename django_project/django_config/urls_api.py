from django.urls import path
from pokemon_app.views_api import (
    create_team_api,
    delete_team_api,
    edit_team_api,
    pokemon_api,
    team_analysis_api,
    teams_api,
    top_pokemon_usage_api,
    top_type_usage_api,
)

urlpatterns = [
    path('pokemon/', pokemon_api, name='pokemon_api'),
    path('team/create/', create_team_api, name='create_team_api'),
    path('team/<int:team_id>/edit/', edit_team_api, name='edit_team_api'),
    path('team/<int:team_id>/delete/', delete_team_api, name='delete_team_api'),
    path('team/<int:team_id>/analysis/', team_analysis_api, name='team_analysis_api'),
    path('teams/', teams_api, name='teams_api'),
    path('stats/top-pokemon/', top_pokemon_usage_api, name='top_pokemon_usage_api'),
    path('stats/top-types/', top_type_usage_api, name='top_type_usage_api'),
]
