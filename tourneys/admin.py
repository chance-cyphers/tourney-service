from django.contrib import admin

# Register your models here.
from tourneys.models import Tourney, Contestant, Character, RoundContestant

admin.site.register(Tourney)
admin.site.register(Contestant)
admin.site.register(Character)
admin.site.register(RoundContestant)
