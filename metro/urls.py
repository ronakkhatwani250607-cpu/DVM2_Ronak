from django.urls import path
from . import views

urlpatterns = [
    path('stations/', views.stations_view, name='stations'),
    path('lines/', views.lines_view, name='lines'),
]