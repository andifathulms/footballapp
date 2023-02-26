from django.urls import path

from . import views


app_name = "regions"

urlpatterns = [
    path('player-by-region', views.player_by_region, name="player_by_region"),
]
