from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bracket/example', views.example_bracket, name='bracketExample'),
    path('tourney/<int:tourney_id>', views.single_tourney),
    path('tourney', views.tourney),
    path('match/<int:match_id>/round-contestant/<int:rc_id>/user/<username>/vote', views.vote),
]
