from django.db import models
from teams.models import Team


class Competition(models.Model):
    name = models.CharField(max_length=255)
    season = models.CharField(max_length=20)
    participated_teams = models.ManyToManyField(Team, related_name='competitions')

    def __str__(self) -> str:
        return self.name + " " + self.season
