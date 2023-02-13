from django.contrib import admin

from .models import *

admin.site.register(Match)
admin.site.register(MatchOfficial)
admin.site.register(MatchData)
admin.site.register(Referee)
admin.site.register(Formation)
admin.site.register(LineUp)
admin.site.register(Substitution)
admin.site.register(Goals)
admin.site.register(MissedPenalty)
admin.site.register(MatchCards)
admin.site.register(PlayerRole)
admin.site.register(PlayerRoleProxy)
