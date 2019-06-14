from django.urls import path

from . import views

urlpatterns = [
    path('bracket/example', views.example_bracket, name='bracketExample'),
    path('', views.index, name='index'),
]
