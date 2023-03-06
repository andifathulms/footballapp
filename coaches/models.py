from django.db import models
from regions.models import Country

from typing import Any


class Coach(models.Model):
    name = models.CharField(max_length=255)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @property
    def get_current_teams(self) -> Any:  # getting past circular import
        return self.teams.first()
