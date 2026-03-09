from django.urls import path
from pokemon_app.views_frontend import index_page, pokemon_page, create_team_page, teams_page, edit_team_page

urlpatterns = [
    path('', index_page, name='index'),
    path('pokemon/', pokemon_page, name='pokemon_page'),
    path('team/create/', create_team_page, name='create_team_page'),
    path('team/<int:team_id>/edit/', edit_team_page, name='edit_team_page'),
    path('teams/', teams_page, name='teams_page'),
]
