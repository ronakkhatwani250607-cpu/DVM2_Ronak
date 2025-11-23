from django.contrib import admin
from django.urls import path, include
from metro.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home, name='home'),
    path('users/', include('users.urls')),
    path('metro/', include('metro.urls')),
    path('tickets/', include('tickets.urls')),
]