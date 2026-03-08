"""
URL configuration for django_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pokemon_app.views_api import pokemon_api
from pokemon_app.views_frontend import index_page, pokemon_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='index'),
    path('api/pokemon/', pokemon_api, name='pokemon_api'),
    path('pokemon/', pokemon_page, name='pokemon_page'),
]
