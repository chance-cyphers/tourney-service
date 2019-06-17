from django.contrib import admin

# Register your models here.
from tourneys.models import Tourney, Character, RoundContestant

admin.site.register(Tourney)
admin.site.register(Character)
admin.site.register(RoundContestant)
