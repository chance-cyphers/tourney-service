from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bracket/example', views.example_bracket, name='bracketExample'),
    path('tourney/<int:tourney_id>', views.single_tourney),
    path('tourney', views.tourneys),
    path('match/<int:match_id>/user/<username>/character/<int:character_id>/vote', views.vote),
    path('tourney/<int:tourney_id>/current-match', views.current_match),
]
