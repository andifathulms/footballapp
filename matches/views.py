from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.urls import reverse

from django.core.paginator import Paginator

from .models import Match
from competitions.models import Competition

from .forms import MatchCreationForm


def index(request: HttpRequest) -> HttpResponse:
    competition = Competition.objects.first()
    matches = Match.objects.filter(competition=competition) \
        .order_by('gameweek', 'match_datas__kick_off_time')

    page = request.GET.get('page', 1)
    paginator = Paginator(matches, per_page=10)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page)

    context_data = {
        "competition": competition,
        "matches": page_object
    }
    return render(request, "matches/index.html", context_data)

def add(request: HttpRequest) -> HttpResponse:

    form = MatchCreationForm(data=request.POST or None)
    if form.is_valid():
        match = form.save()
        messages.success(request, f"Macth successfully created. {match.home_team} vs {match.away_team}")
        return redirect(reverse("matches:add"))

    context_data = {
        "title": "Add Match",
        "current_page": "matches",
        "form": form
    }
    return render(request, "matches/add.html", context_data)
