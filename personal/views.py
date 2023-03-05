from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import F, Sum, Case, When, OuterRef

from matches.models import Match
from competitions.models import Competition


def index(request: HttpRequest) -> HttpResponse:
    competition = Competition.objects.first()

    qs_match = Match.objects.filter(competition=competition, gameweek__lte=34)
    qs_home = qs_match.values(name=F("home_team__name")) \
        .annotate(home_win=Sum(Case(When(home_score__gt=F('away_score'), then=1)), default=0),
                  home_draw=Sum(Case(When(home_score=F('away_score'), then=1)), default=0),
                  home_lose=Sum(Case(When(home_score__lt=F('away_score'), then=1)), default=0),
                  home_goal=Sum('home_score', default=0),
                  home_conceded=Sum('away_score', default=0),
                  home_point=Sum(Case(When(home_score__gt=F('away_score'), then=3),
                                      When(home_score=F('away_score'), then=1)
                                ), default=0)
        ).filter(name=OuterRef('team'))

    qs_away = qs_match.values(name=F("away_team__name")) \
        .annotate(away_win=Sum(Case(When(away_score__gt=F('home_score'), then=1)), default=0),
                  away_draw=Sum(Case(When(away_score=F('home_score'), then=1)), default=0),
                  away_lose=Sum(Case(When(away_score__lt=F('home_score'), then=1)), default=0),
                  away_goal=Sum('away_score', default=0),
                  away_conceded=Sum('home_score', default=0),
                  away_point=Sum(Case(When(away_score__gt=F('home_score'), then=3),
                                      When(away_score=F('home_score'), then=1)
                                ), default=0)
        ).filter(name=OuterRef('team'))

    merged_qs = competition.participated_teams.values(team=F("name")) \
        .annotate(home_win=qs_home.values('home_win'),
                  home_draw=qs_home.values('home_draw'),
                  home_lose=qs_home.values('home_lose'),
                  home_goal=qs_home.values('home_goal'),
                  home_conceded=qs_home.values('home_conceded'),
                  home_difference=F('home_goal') - F('home_conceded'),
                  home_point=qs_home.values('home_point'),
                  home_played=F('home_win') + F('home_draw') + F('home_lose'),
                  away_win=qs_away.values('away_win'),
                  away_draw=qs_away.values('away_draw'),
                  away_lose=qs_away.values('away_lose'),
                  away_goal=qs_away.values('away_goal'),
                  away_conceded=qs_away.values('away_conceded'),
                  away_difference=F('away_goal') - F('away_conceded'),
                  away_point=qs_away.values('away_point'),
                  away_played=F('away_win') + F('away_draw') + F('away_lose'),
                  total_win=F('home_win') + F('away_win'),
                  total_draw=F('home_draw') + F('away_draw'),
                  total_lose=F('home_lose') + F('away_lose'),
                  total_goal=F('home_goal') + F('away_goal'),
                  total_conceded=F('home_conceded') + F('away_conceded'),
                  total_difference=F('home_difference') + F('away_difference'),
                  total_point=F('home_point') + F('away_point'),
                  total_played=F('home_played') + F('away_played')) \
        .order_by('-total_point', '-total_difference', '-total_goal')

    context_data = {
        "tables": merged_qs
    }
    return render(request, 'main.html', context_data)
