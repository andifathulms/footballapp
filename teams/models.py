from django.db import models
from stadiums.models import Stadium
from regions.models import City
from coaches.models import Coach
from players.models import Player

from model_utils import Choices


class Team(models.Model):
    name = models.CharField(max_length=255)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='teams', on_delete=models.CASCADE)
    coaches = models.ManyToManyField(Coach, through='CoachList', related_name='teams')
    players = models.ManyToManyField(Player, through='PlayerList', related_name='teams')

    def __str__(self) -> str:
        return self.name


class CoachList(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    DEPARTURE_REASON = Choices(
        (1, 'sacked', 'Sacked'), 
        (2, 'mutual_consent', 'Mutual Consent'),
        (3, 'resigned', 'Resigned'),
        (4, 'end_of_caretaker_spell', 'End of Caretaker Spell'),
        (4, 'end_of_contract', 'End of Contract')
    )
    departure_reason = models.PositiveSmallIntegerField(choices=DEPARTURE_REASON, blank=True, null=True)

    STATUS = Choices(
        (1, 'manager', 'Manager'),
        (2, 'caretaker', 'Caretaker')
    )
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.manager)

    def __str__(self) -> str:
        return f"{self.coach.name} ({self.team.name})"


class PlayerList(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    shirt_number = models.PositiveSmallIntegerField(blank=True, null=True )
    is_active = models.BooleanField(default=True)

    STATUS = Choices(
        (1, 'permanent', 'Permanent'),
        (2, 'on_loan', 'On Loan'),
        (3, 'youth', 'Youth')
    )
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.permanent)

    def __str__(self) -> str:
        return f"{self.player.name} ({self.team.name})"
