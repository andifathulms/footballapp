from django import forms

from .models import Position, Player
from teams.models import PlayerList, Team
from regions.models import City, Country

from typing import List, Any


class PlayerCreationForm(forms.Form):
    name = forms.CharField()
    fullname = forms.CharField(required=False)
    nationality = forms.ModelChoiceField(queryset=None)
    date_of_birth = forms.DateField(required=False)
    place_of_birth = forms.ModelChoiceField(queryset=None, required=False)
    height = forms.IntegerField(required=False)
    primary_position = forms.ModelChoiceField(queryset=None)
    other_position = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(), required=False)
    preferred_foot = forms.TypedChoiceField(choices=Player.PREFERRED_FOOT, coerce=int, initial=Player.PREFERRED_FOOT.R, required=False)

    team = forms.ModelChoiceField(queryset=None)
    start_date = forms.DateField()
    end_date = forms.DateField(required=False)
    shirt_number = forms.IntegerField()
    status = forms.TypedChoiceField(choices=PlayerList.STATUS, coerce=int, initial=PlayerList.STATUS.permanent)

    def __init__(self, *args: List, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        countries = Country.objects.order_by('name')
        initial_country = Country.objects.get(name="Indonesia")
        self.fields['nationality'].queryset = countries
        self.fields['nationality'].initial = initial_country

        cities = City.objects.order_by('type', 'name')
        self.fields['place_of_birth'].queryset = cities

        positions = Position.objects.order_by('-display_order')
        self.fields['primary_position'].queryset = positions
        self.fields['other_position'].queryset = positions

        teams = Team.objects.order_by('name')
        initial_team = Team.objects.get(name="Barito Putera")
        self.fields['team'].queryset = teams
        self.fields['team'].initial = initial_team
    
    def save(self) -> Player:
        name = self.cleaned_data["name"]
        fullname = self.cleaned_data["fullname"]
        nationality = self.cleaned_data["nationality"]
        date_of_birth = self.cleaned_data["date_of_birth"]
        place_of_birth = self.cleaned_data["place_of_birth"]
        height = self.cleaned_data["height"]
        primary_position = self.cleaned_data["primary_position"]
        other_position = self.cleaned_data["other_position"]
        preferred_foot = self.cleaned_data["preferred_foot"]

        team = self.cleaned_data["team"]
        start_date = self.cleaned_data["start_date"]
        end_date = self.cleaned_data["end_date"]
        shirt_number = self.cleaned_data["shirt_number"]
        status = self.cleaned_data["status"]

        player = Player.objects.create(
            name=name, fullname=fullname, nationality=nationality, date_of_birth=date_of_birth,
            place_of_birth=place_of_birth, height=height, primary_position=primary_position,
            preferred_foot=preferred_foot
        )

        player.other_position.set(other_position)

        PlayerList.objects.create(
            team=team, player=player, start=start_date, end=end_date,
            shirt_number=shirt_number, status=status
        )

        return player
