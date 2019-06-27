from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bracket/example', views.example_bracket, name='bracketExample'),
    path('tourney/<int:tourney_id>', views.single_tourney),
    path('tourney', views.tourneys),
    path('v2/tourney', views.tourneys_v2),
    path('match/<int:match_id>/character/<int:character_id>/vote', views.vote),
    path('tourney/<int:tourney_id>/current-match', views.current_match),
]
