from django.contrib import admin

# Register your models here.
from tourneys.models import Tourney, Contestant

admin.site.register(Tourney)
admin.site.register(Contestant)
