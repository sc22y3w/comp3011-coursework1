from django.urls import path
from pokemon_app.views_api import pokemon_api, create_team_api, teams_api, edit_team_api, delete_team_api

urlpatterns = [
    path('pokemon/', pokemon_api, name='pokemon_api'),
    path('team/create/', create_team_api, name='create_team_api'),
    path('team/<int:team_id>/edit/', edit_team_api, name='edit_team_api'),
    path('team/<int:team_id>/delete/', delete_team_api, name='delete_team_api'),
    path('teams/', teams_api, name='teams_api'),
]
