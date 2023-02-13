from django.db import models
from stadiums.models import Stadium
from regions.models import City
from coaches.models import Coach
from players.models import Player

from model_utils import Choices


class Team(models.Model):
    name = models.CharField(max_length=255)
    stadium = models.OneToOneField(Stadium, on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='teams', on_delete=models.CASCADE)
    coaches = models.ManyToManyField(Coach, through='CoachList', related_name='teams')
    players = models.ManyToManyField(Player, through='PlayerList', related_name='teams')


class CoachList(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    DEPARTURE_REASON = Choices(
        (1, 'sacked', 'Sacked'), 
        (2, 'mutual_consent', 'Mutual Consent')
    )
    departure_reason = models.PositiveSmallIntegerField(choices=DEPARTURE_REASON, blank=True, null=True)


class PlayerList(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    shirt_number = models.PositiveSmallIntegerField(blank=True, null=True )
    is_active = models.BooleanField(default=True)
