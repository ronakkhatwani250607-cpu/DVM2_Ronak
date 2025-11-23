from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup_redirect, name='signup_redirect'),
    path('add-money/', views.add_money, name='add_money'),
]