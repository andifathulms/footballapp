from django.db import models
from regions.models import Country, City

from model_utils import Choices

from typing import Any


class Player(models.Model):
    name = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    place_of_birth = models.ForeignKey(City, related_name='players', on_delete=models.CASCADE, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    primary_position = models.ForeignKey('Position', related_name='primary_position_players', on_delete=models.CASCADE)
    other_position = models.ManyToManyField('Position', related_name='other_position_players', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    PREFERRED_FOOT = Choices(
        (1, 'L', 'Left'),
        (2, 'R', 'Right')
    )
    preferred_foot = models.PositiveSmallIntegerField(choices=PREFERRED_FOOT, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @property
    def get_current_teams(self) -> Any:  # getting past circular import
        # print(self.teams.first().start)
        return self.teams.first()

class Position(models.Model):
    name = models.CharField(max_length=20, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True, db_index=True)
    
    TYPE = Choices(
        (1, 'FW', 'Forward'),
        (2, 'MF', 'Midfielder'),
        (3, 'DF', 'Defender'),
        (4, 'GK', 'Goalkeeper')
    )
    type = models.PositiveSmallIntegerField(choices=TYPE)
    display_order = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.abbreviation
