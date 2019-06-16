from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bracket/example', views.example_bracket, name='bracketExample'),
    path('tourney', views.tourneys),
    path('tourney/<int:tourney_id>/', views.single_tourney),
]
