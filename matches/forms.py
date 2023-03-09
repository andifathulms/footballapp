from django import forms

from .models import Match, MatchData, Formation
from competitions.models import Competition
from teams.models import Team, PlayerList, CoachList
from stadiums.models import Stadium
from coaches.models import Coach
from players.models import Position

from typing import List, Any, Dict


class MatchCreationForm(forms.ModelForm):
    competition = forms.ModelChoiceField(queryset=None)
    home_team = forms.ModelChoiceField(queryset=None)
    away_team = forms.ModelChoiceField(queryset=None)
    status = forms.TypedChoiceField(choices=Match.STATUS, coerce=int, initial=Match.STATUS.full_time)

    class Meta:
        model = Match
        fields = ('__all__')

    def __init__(self, *args: List, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        competitions = Competition.objects.all()
        initial_competition = competitions.first()
        self.fields['competition'].queryset = competitions
        self.fields['competition'].initial = initial_competition

        teams = Team.objects.order_by('name')
        self.fields['home_team'].queryset = teams
        self.fields['away_team'].queryset = teams

        self.fields['gameweek'].initial = 29

    def clean(self) -> Dict:
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        competition = cleaned_data['competition']
        home_team = cleaned_data['home_team']
        away_team = cleaned_data['away_team']

        if Match.objects.filter(home_team=home_team, away_team=away_team, competition=competition).exists():
            raise forms.ValidationError(f"This match already exist in this competition", code="invalid_match")

        if home_team == away_team:
            raise forms.ValidationError(f"Invalid teams", code="invalid_team")

        return cleaned_data

    def save(self, *args: List, **kwargs: Any) -> None:
        match = super().save(*args, **kwargs)

        return match


class MatchDataCreationForm(forms.Form):
    kick_off_time = forms.DateTimeField()
    stadium = forms.ModelChoiceField(queryset=None)
    attendance = forms.IntegerField()
    first_half_added_time = forms.IntegerField()
    second_half_added_time = forms.IntegerField()

    home_coach = forms.ModelChoiceField(queryset=None)
    home_formation = forms.ModelChoiceField(queryset=None)

    home_first_starting = forms.ModelChoiceField(queryset=None)
    home_second_starting = forms.ModelChoiceField(queryset=None)
    home_third_starting = forms.ModelChoiceField(queryset=None)
    home_fourth_starting = forms.ModelChoiceField(queryset=None)
    home_fifth_starting = forms.ModelChoiceField(queryset=None)
    home_sixth_starting = forms.ModelChoiceField(queryset=None)
    home_seventh_starting = forms.ModelChoiceField(queryset=None)
    home_eighth_starting = forms.ModelChoiceField(queryset=None)
    home_ninth_starting = forms.ModelChoiceField(queryset=None)
    home_tenth_starting = forms.ModelChoiceField(queryset=None)
    home_eleventh_starting = forms.ModelChoiceField(queryset=None)

    home_first_starting_position = forms.ModelChoiceField(queryset=None)
    home_second_starting_position = forms.ModelChoiceField(queryset=None)
    home_third_starting_position = forms.ModelChoiceField(queryset=None)
    home_fourth_starting_position = forms.ModelChoiceField(queryset=None)
    home_fifth_starting_position = forms.ModelChoiceField(queryset=None)
    home_sixth_starting_position = forms.ModelChoiceField(queryset=None)
    home_seventh_starting_position = forms.ModelChoiceField(queryset=None)
    home_eighth_starting_position = forms.ModelChoiceField(queryset=None)
    home_ninth_starting_position = forms.ModelChoiceField(queryset=None)
    home_tenth_starting_position = forms.ModelChoiceField(queryset=None)
    home_eleventh_starting_position = forms.ModelChoiceField(queryset=None)

    away_coach = forms.ModelChoiceField(queryset=None)
    away_formation = forms.ModelChoiceField(queryset=None)

    away_first_starting = forms.ModelChoiceField(queryset=None)
    away_second_starting = forms.ModelChoiceField(queryset=None)
    away_third_starting = forms.ModelChoiceField(queryset=None)
    away_fourth_starting = forms.ModelChoiceField(queryset=None)
    away_fifth_starting = forms.ModelChoiceField(queryset=None)
    away_sixth_starting = forms.ModelChoiceField(queryset=None)
    away_seventh_starting = forms.ModelChoiceField(queryset=None)
    away_eighth_starting = forms.ModelChoiceField(queryset=None)
    away_ninth_starting = forms.ModelChoiceField(queryset=None)
    away_tenth_starting = forms.ModelChoiceField(queryset=None)
    away_eleventh_starting = forms.ModelChoiceField(queryset=None)

    away_first_starting_position = forms.ModelChoiceField(queryset=None)
    away_second_starting_position = forms.ModelChoiceField(queryset=None)
    away_third_starting_position = forms.ModelChoiceField(queryset=None)
    away_fourth_starting_position = forms.ModelChoiceField(queryset=None)
    away_fifth_starting_position = forms.ModelChoiceField(queryset=None)
    away_sixth_starting_position = forms.ModelChoiceField(queryset=None)
    away_seventh_starting_position = forms.ModelChoiceField(queryset=None)
    away_eighth_starting_position = forms.ModelChoiceField(queryset=None)
    away_ninth_starting_position = forms.ModelChoiceField(queryset=None)
    away_tenth_starting_position = forms.ModelChoiceField(queryset=None)
    away_eleventh_starting_position = forms.ModelChoiceField(queryset=None)

    def __init__(self, match: Match, *args: List, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.match = match

        stadiums = Stadium.objects.all()
        initial_stadium = match.home_team.stadium
        self.fields['stadium'].queryset = stadiums
        self.fields['stadium'].initial = initial_stadium

        home_players = PlayerList.objects.filter(team=match.home_team)
        away_players = PlayerList.objects.filter(team=match.away_team)
        home_coaches = CoachList.objects.filter(team=match.home_team)
        away_coaches = CoachList.objects.filter(team=match.away_team)
        formations = Formation.objects.all()
        positions = Position.objects.all()

        self.fields['home_coach'].queryset = home_coaches
        self.fields['home_formation'].queryset = formations
        self.fields['home_first_starting'].queryset = home_players.filter(player__primary_position__type=Position.TYPE.GK)
        self.fields['home_second_starting'].queryset = home_players
        self.fields['home_third_starting'].queryset = home_players
        self.fields['home_fourth_starting'].queryset = home_players
        self.fields['home_fifth_starting'].queryset = home_players
        self.fields['home_sixth_starting'].queryset = home_players
        self.fields['home_seventh_starting'].queryset = home_players
        self.fields['home_eighth_starting'].queryset = home_players
        self.fields['home_ninth_starting'].queryset = home_players
        self.fields['home_tenth_starting'].queryset = home_players
        self.fields['home_eleventh_starting'].queryset = home_players

        self.fields['home_first_starting_position'].queryset = positions
        self.fields['home_second_starting_position'].queryset = positions
        self.fields['home_third_starting_position'].queryset = positions
        self.fields['home_fourth_starting_position'].queryset = positions
        self.fields['home_fifth_starting_position'].queryset = positions
        self.fields['home_sixth_starting_position'].queryset = positions
        self.fields['home_seventh_starting_position'].queryset = positions
        self.fields['home_eighth_starting_position'].queryset = positions
        self.fields['home_ninth_starting_position'].queryset = positions
        self.fields['home_tenth_starting_position'].queryset = positions
        self.fields['home_eleventh_starting_position'].queryset = positions

        self.fields['away_coach'].queryset = away_coaches
        self.fields['away_formation'].queryset = formations
        self.fields['away_first_starting'].queryset = away_players.filter(player__primary_position__type=Position.TYPE.GK)
        self.fields['away_second_starting'].queryset = away_players
        self.fields['away_third_starting'].queryset = away_players
        self.fields['away_fourth_starting'].queryset = away_players
        self.fields['away_fifth_starting'].queryset = away_players
        self.fields['away_sixth_starting'].queryset = away_players
        self.fields['away_seventh_starting'].queryset = away_players
        self.fields['away_eighth_starting'].queryset = away_players
        self.fields['away_ninth_starting'].queryset = away_players
        self.fields['away_tenth_starting'].queryset = away_players
        self.fields['away_eleventh_starting'].queryset = away_players

        self.fields['away_first_starting_position'].queryset = positions
        self.fields['away_second_starting_position'].queryset = positions
        self.fields['away_third_starting_position'].queryset = positions
        self.fields['away_fourth_starting_position'].queryset = positions
        self.fields['away_fifth_starting_position'].queryset = positions
        self.fields['away_sixth_starting_position'].queryset = positions
        self.fields['away_seventh_starting_position'].queryset = positions
        self.fields['away_eighth_starting_position'].queryset = positions
        self.fields['away_ninth_starting_position'].queryset = positions
        self.fields['away_tenth_starting_position'].queryset = positions
        self.fields['away_eleventh_starting_position'].queryset = positions
    
    def save(self, *args: List, **kwargs: Any) -> MatchData:
        pass
