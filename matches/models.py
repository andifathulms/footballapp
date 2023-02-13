from django.db import models

from competitions.models import Competition
from teams.models import Team
from coaches.models import Coach
from players.models import Player, Position
from regions.models import Country
from stadiums.models import Stadium

from model_utils import Choices


class Match(models.Model):
    competition = models.ForeignKey(Competition, related_name='matches', on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    home_score = models.PositiveSmallIntegerField(default=0)
    away_score = models.PositiveSmallIntegerField(default=0)

    STATUS = Choices(
        (1, 'not_started', 'Not Started'),
        (2, 'half_time', 'Half Time'),
        (3, 'full_time', 'Full Time'),
        (9, 'postponed', 'Postponed')
    )
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.not_started)


class MatchOfficial(models.Model):
    match = models.OneToOneField('Match', related_name='match_officials', on_delete=models.CASCADE)
    referee = models.ForeignKey('Referee', related_name='main_officials', on_delete=models.CASCADE)
    first_assistant_referee = models.ForeignKey('Referee', related_name='first_assistant_officials', on_delete=models.CASCADE, blank=True, null=True)
    second_assistant_referee = models.ForeignKey('Referee', related_name='second_assistant_officials', on_delete=models.CASCADE, blank=True, null=True)
    first_additional_referee = models.ForeignKey('Referee', related_name='first_additional_officials', on_delete=models.CASCADE, blank=True, null=True)
    second_additional_referee = models.ForeignKey('Referee', related_name='second_additional_officials', on_delete=models.CASCADE, blank=True, null=True)
    reserve_referee = models.ForeignKey('Referee', related_name='reserve_officials', on_delete=models.CASCADE, blank=True, null=True)


class MatchData(models.Model):
    match = models.OneToOneField('Match', related_name='match_datas', on_delete=models.CASCADE)
    kick_off_time = models.DateTimeField()  # local time
    stadium = models.ForeignKey(Stadium, related_name='match_datas', on_delete=models.CASCADE)
    attendance = models.IntegerField()
    first_half_added_time = models.PositiveSmallIntegerField()
    second_half_added_time = models.PositiveSmallIntegerField()
    et_first_half_added_time = models.PositiveSmallIntegerField(blank=True, null=True)
    et_second_half_added_time = models.PositiveSmallIntegerField(blank=True, null=True)
    cards = models.ManyToManyField(Player, related_name='match_datas', through='MatchCards')
    lineups = models.ForeignKey('LineUp', related_name='match_datas', on_delete=models.CASCADE)


class Referee(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.ForeignKey(Country, related_name='referees', on_delete=models.CASCADE)


class Formation(models.Model):
    name = models.CharField(max_length=10)


class LineUp(models.Model):
    coach = models.ForeignKey(Coach, related_name='match_lineups', on_delete=models.CASCADE)
    formation = models.ForeignKey(Formation, related_name='match_lineups', on_delete=models.CASCADE)
    starting = models.ManyToManyField(Player, related_name='match_starting_lineups', through='PlayerRoleProxy')
    reserved = models.ManyToManyField(Player, related_name='match_reserved_lineups', through='PlayerRole')

    TYPE = Choices(
        (1, 'home', 'Home'),
        (2, 'away', 'Away')
    )
    type = models.PositiveSmallIntegerField(choices=TYPE)


class Substitution(models.Model):
    match = models.ForeignKey('Match', related_name='substitutions', on_delete=models.CASCADE)
    player_out = models.ForeignKey(Player, related_name='out_substitutions', on_delete=models.CASCADE)
    player_in = models.ForeignKey(Player, related_name='in_substitutions', on_delete=models.CASCADE)

    HALF = Choices(
        (1, 'first_half', 'First Half'),
        (2, 'second_half', 'Second Half'),
        (3, 'first_half_et', 'Extra Time First Half'),
        (4, 'second_half_et', 'Extra Time Second Half')
    )
    half = models.PositiveSmallIntegerField(choices=HALF)

    minute = models.PositiveIntegerField()


class Goals(models.Model):
    match = models.ForeignKey('Match', related_name='goals', on_delete=models.CASCADE)
    scorer = models.ForeignKey(Player, related_name='goal_scorers', on_delete=models.CASCADE)
    assist = models.ForeignKey(Player, related_name='goal_assists', on_delete=models.CASCADE, blank=True, null=True)
    second_assist = models.ForeignKey(Player, related_name='goal_second_assists', on_delete=models.CASCADE, blank=True, null=True)

    HALF = Choices(
        (1, 'first_half', 'First Half'),
        (2, 'second_half', 'Second Half'),
        (3, 'first_half_et', 'Extra Time First Half'),
        (4, 'second_half_et', 'Extra Time Second Half'),
        (5, 'penaltiy_shootout', 'Penalty Shoot-Out')
    )
    half = models.PositiveSmallIntegerField(choices=HALF)

    minute = models.PositiveIntegerField()

    BODY_PART = Choices(
        (1, 'head', 'Head'),
        (2, 'left_foot', 'Left Foot'),
        (3, 'right_foot', 'Right Foot'),
        (9, 'other', 'Other')
    )
    goal_body_part = models.PositiveSmallIntegerField(choices=BODY_PART)
    assist_body_part = models.PositiveSmallIntegerField(choices=BODY_PART, blank=True, null=True)

    CATEGORY = Choices(
        (1, 'progressive_pass', 'Progressive Pass'),
        (2, 'basic_pass', 'Basic Pass'),
        (3, 'set_piece_pass', 'Set Piece Pass'),
        (4, 'set_piece_kick', 'Set Piece Kick'),
        (5, 'individual_play', 'Individual Play'),
        (9, 'own_goal', 'Own Goal'),
    )
    category = models.PositiveSmallIntegerField(choices=CATEGORY)

    AREA_OF_SHOOT = Choices(
        (1, '6_yard_box', '6 Yard Box'),
        (2, 'penalty_box', 'Penalty Box'),
        (3, 'outside_penalty_box', 'Outside Penalty Box')
    )
    area_of_shoot = models.PositiveSmallIntegerField(choices=AREA_OF_SHOOT)

    SET_PIECES_TYPE = Choices(
        (1, 'free_kick', 'Free Kick'),
        (2, 'corner_kick', 'Corner Kick'),
        (3, 'penalty_kick', 'Penalty Kick'),
        (4, 'throw_in', 'Throw In')
    )
    set_pieces_type = models.PositiveSmallIntegerField(choices=SET_PIECES_TYPE, blank=True, null=True)

    ATTACKING_FLANKS = Choices(
        (1, 'left', 'Left'),
        (2, 'right', 'Right')
    )
    attacking_flanks = models.PositiveSmallIntegerField(choices=ATTACKING_FLANKS, blank=True, null=True)

    is_deflected = models.BooleanField(default=False)
    error_leading_to_goal = models.BooleanField(default=False)

    ASSIST_PASS_TYPE = Choices(
        (1, 'cross', 'Cross'),
        (2, 'deep_completed_cross', 'Deep Completed Cross'),
        (3, 'deflected_cross', 'Deflected Cross'),
        (4, 'deep_completion', 'Deep Completion'),
        (5, 'head_pass', 'Head Pass'),
        (6, 'progressive_pass', 'Progressive Pass'),
        (90, 'rebound', 'Rebound')
    )
    assist_pass_type = models.PositiveSmallIntegerField(choices=ASSIST_PASS_TYPE, blank=True, null=True)


class MissedPenalty(models.Model):
    match = models.ForeignKey('Match', related_name='missed_penalties', on_delete=models.CASCADE)
    penalty_taker = models.ForeignKey(Player, related_name='missed_penalties', on_delete=models.CASCADE)

    TYPE = Choices(
        (1, 'saved', 'Saved'),
        (2, 'missed', 'Missed'),
        (3, 'hit_the_crossbar', 'Hit the Crossbar'),
    )
    type = models.PositiveSmallIntegerField(choices=TYPE)

    HALF = Choices(
        (1, 'first_half', 'First Half'),
        (2, 'second_half', 'Second Half'),
        (3, 'first_half_et', 'Extra Time First Half'),
        (4, 'second_half_et', 'Extra Time Second Half'),
        (5, 'penaltiy_shootout', 'Penalty Shoot-Out')
    )
    half = models.PositiveSmallIntegerField(choices=HALF)

    minute = models.PositiveIntegerField()


class MatchCards(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match_data = models.ForeignKey('MatchData', on_delete=models.CASCADE)

    HALF = Choices(
        (1, 'first_half', 'First Half'),
        (2, 'second_half', 'Second Half'),
        (3, 'first_half_et', 'Extra Time First Half'),
        (4, 'second_half_et', 'Extra Time Second Half')
    )
    half = models.PositiveSmallIntegerField(choices=HALF)

    TYPE = Choices(
        (1, 'yellow', 'Yellow'),
        (2, 'second_yellow', 'Yellow'),
        (3, 'red', 'Red'),
    )
    type = models.PositiveSmallIntegerField(choices=TYPE)

    minute = models.PositiveIntegerField()

    
class PlayerRole(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    lineup = models.ForeignKey('Lineup', on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    is_captain = models.BooleanField(default=False)


class PlayerRoleProxy(PlayerRole):
    class Meta:
        proxy = True
