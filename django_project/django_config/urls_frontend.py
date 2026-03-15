from django.urls import path
from pokemon_app.views_frontend import (
    analysis_page,
    create_team_page,
    edit_team_page,
    global_stats_page,
    index_page,
    login_page,
    pokemon_page,
    register_page,
    teams_page,
)

urlpatterns = [
    path('', index_page, name='index'),
    path('login/', login_page, name='frontend_login'),
    path('register/', register_page, name='frontend_register'),
    path('pokemon/', pokemon_page, name='pokemon_page'),
    path('team/create/', create_team_page, name='create_team_page'),
    path('team/<int:team_id>/edit/', edit_team_page, name='edit_team_page'),
    path('team/<int:team_id>/analysis/', analysis_page, name='analysis_page'),
    path('teams/', teams_page, name='teams_page'),
    path('global-stats/', global_stats_page, name='global_stats_page'),
]
