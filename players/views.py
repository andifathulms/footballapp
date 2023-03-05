from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.urls import reverse

from django.core.paginator import Paginator

from .models import Player
from .forms import PlayerCreationForm


def index(request: HttpRequest) -> HttpResponse:
    players = Player.objects.order_by('name')

    page = request.GET.get('page', 1)
    paginator = Paginator(players, per_page=10)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page)

    context_data = {
        "players": page_object
    }
    return render(request, "players/index.html", context_data)

def add(request: HttpRequest) -> HttpResponse:

    form = PlayerCreationForm(data=request.POST or None)
    if form.is_valid():
        player = form.save()
        messages.success(request, f"Player successfully created. {player} ({player.get_current_teams})")
        return redirect(reverse("players:add"))

    context_data = {
        "title": "Add Player",
        "current_page": "players",
        "form": form
    }
    return render(request, "players/add.html", context_data)
