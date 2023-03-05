from django import forms

from .models import Match
from competitions.models import Competition
from teams.models import Team

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

        self.fields['gameweek'].initial = 28

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
