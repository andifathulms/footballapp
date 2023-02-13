from django.contrib import admin

from .models import Team, PlayerList, CoachList

admin.site.register(Team)
admin.site.register(PlayerList)
admin.site.register(CoachList)
