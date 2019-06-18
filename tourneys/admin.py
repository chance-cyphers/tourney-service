from django.contrib import admin

# Register your models here.
from tourneys.models import Tourney, Character, RoundContestant, Vote, Match

admin.site.register(Tourney)
admin.site.register(Character)
admin.site.register(RoundContestant)
admin.site.register(Vote)
admin.site.register(Match)
