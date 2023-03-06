from django import forms

from .models import Coach
from teams.models import Team, CoachList
from regions.models import Country

from typing import List, Any


class CoachCreationForm(forms.Form):
    name = forms.CharField()
    nationality = forms.ModelChoiceField(queryset=None)
    date_of_birth = forms.DateField(required=False)
    height = forms.IntegerField(required=False)

    team = forms.ModelChoiceField(queryset=None)
    start_date = forms.DateField()
    end_date = forms.DateField(required=False)
    status = forms.TypedChoiceField(choices=CoachList.STATUS, coerce=int, initial=CoachList.STATUS.manager)
    departure_reason = forms.TypedChoiceField(choices=[("", "----")] + CoachList.DEPARTURE_REASON, coerce=int, required=False)

    def __init__(self, *args: List, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        countries = Country.objects.order_by('name')
        self.fields['nationality'].queryset = countries

        teams = Team.objects.order_by('name')
        self.fields['team'].queryset = teams

    def save(self) -> Coach:
        name = self.cleaned_data["name"]
        nationality = self.cleaned_data["nationality"]
        date_of_birth = self.cleaned_data["date_of_birth"]
        height = self.cleaned_data["height"]

        team = self.cleaned_data["team"]
        start_date = self.cleaned_data["start_date"]
        end_date = self.cleaned_data["end_date"]
        status = self.cleaned_data["status"]
        departure_reason = self.cleaned_data["departure_reason"]

        coach = Coach.objects.create(
            name=name, nationality=nationality, date_of_birth=date_of_birth, height=height
        )

        CoachList.objects.create(
            team=team, coach=coach, start=start_date, end=end_date, status=status,
            departure_reason=departure_reason if departure_reason else None
        )

        return coach
