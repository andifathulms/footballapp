from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.urls import reverse

from django.core.paginator import Paginator

from .models import Match
from competitions.models import Competition

from .forms import MatchCreationForm, MatchDataCreationForm


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

def add_data(request: HttpRequest, id: int) -> HttpResponse:
    match = get_object_or_404(Match.objects.select_related('home_team', 'away_team', 'home_team__stadium'),
                              id=id)

    form = MatchDataCreationForm(data=request.POST or None, match=match)
    if form.is_valid():
        match_data = form.save()
        messages.success(request, f"Macth data successfully created. {match_data.match.home_team} vs {match_data.match.away_team}")
        return redirect(reverse("matches:index"))

    context_data = {
        "title": f"Add Match Data {match.home_team} vs {match.away_team}",
        "current_page": "matches",
        "form": form
    }
    return render(request, "matches/add_data.html", context_data)
