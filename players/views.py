from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.urls import reverse

from .forms import PlayerCreationForm

def add(request: HttpRequest) -> HttpResponse:

    form = PlayerCreationForm(data=request.POST or None)
    if form.is_valid():
        player = form.save()
        messages.success(request, f"Player successfully created. {player} ({player.get_current_teams})")
        # return redirect(reverse("customers:bookings:details", args=[booking.id]))
        return redirect(reverse("players:add"))

    context_data = {
        "title": "Add Player",
        "current_page": "players",
        "form": form
    }
    return render(request, "players/add.html", context_data)
