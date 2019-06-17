from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bracket/example', views.example_bracket, name='bracketExample'),
    path('tourney/<int:tourney_id>', views.single_tourney),
    path('tourney', views.tourney),
    path('tourney/<int:tourney_id>/current_match/user/<username>/vote', views.vote),
]
