from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.db.models import Count, F, Q, Avg, ExpressionWrapper, DurationField
from django.utils import timezone

from players.models import Position, Player
from teams.models import PlayerList


def player_by_region(request: HttpRequest) -> HttpResponse:
    provinces = PlayerList.objects.select_related('player__place_of_birth') \
        .filter(player__place_of_birth__country__name="Indonesia", is_active=True) \
        .values(name=F("player__place_of_birth__province__name")) \
        .annotate(count=Count("id")).annotate(count_team=Count("team", distinct=True)) \
        .annotate(count_regency=Count('player__place_of_birth', distinct=True)) \
        .annotate(count_of_gk=Count('player__primary_position',
                                    filter=Q(player__primary_position__type=Position.TYPE.GK))) \
        .annotate(count_of_df=Count('player__primary_position',
                                    filter=Q(player__primary_position__type=Position.TYPE.DF))) \
        .annotate(count_of_mf=Count('player__primary_position',
                                    filter=Q(player__primary_position__type=Position.TYPE.MF))) \
        .annotate(count_of_fw=Count('player__primary_position',
                                    filter=Q(player__primary_position__type=Position.TYPE.FW))) \
        .annotate(average_height=Avg('player__height')) \
        .annotate(count_of_left_footed=Count('player__preferred_foot',
                                             filter=Q(player__preferred_foot=Player.PREFERRED_FOOT.L))) \
        .annotate(count_of_right_footed=Count('player__preferred_foot',
                                              filter=Q(player__preferred_foot=Player.PREFERRED_FOOT.R))) \
        .annotate(count_of_both_footed=Count('player__preferred_foot',
                                             filter=Q(player__preferred_foot=Player.PREFERRED_FOOT.both))) \
        .annotate(age=Avg(ExpressionWrapper(timezone.now() - F('player__date_of_birth'), output_field=DurationField()))) \
        .order_by('-count')

    foreigners = PlayerList.objects.select_related('player__place_of_birth') \
        .filter(is_active=True).exclude(player__place_of_birth__country__name="Indonesia") \
        .values(name=F("player__place_of_birth__country__name")) \
        .annotate(count=Count("id")).annotate(count_team=Count("team", distinct=True)) \
        .annotate(count_regency=Count('player__place_of_birth', distinct=True)) \
        .annotate(count_of_gk=Count('player__primary_position',
                                    filter=Q(player__primary_position__type=Position.TYPE.GK))) \
        .annotate(count_of_df=Count('player__primary_position',
                                    filter=Q(player__primary_position__type=Position.TYPE.DF))) \
        .annotate(count_of_mf=Count('player__primary_position',
                                    filter=Q(player__primary_position__type=Position.TYPE.MF))) \
        .annotate(count_of_fw=Count('player__primary_position',
                                    filter=Q(player__primary_position__type=Position.TYPE.FW))) \
        .annotate(average_height=Avg('player__height')) \
        .annotate(count_of_left_footed=Count('player__preferred_foot',
                                             filter=Q(player__preferred_foot=Player.PREFERRED_FOOT.L))) \
        .annotate(count_of_right_footed=Count('player__preferred_foot',
                                              filter=Q(player__preferred_foot=Player.PREFERRED_FOOT.R))) \
        .annotate(count_of_both_footed=Count('player__preferred_foot',
                                             filter=Q(player__preferred_foot=Player.PREFERRED_FOOT.both))) \
        .annotate(age=Avg(ExpressionWrapper(timezone.now() - F('player__date_of_birth'), output_field=DurationField()))) \
        .order_by('-count')

    context_data = {
        'provinces': provinces,
        'foreigners': foreigners
    }
    return render(request, "regions/player_by_region.html", context_data)