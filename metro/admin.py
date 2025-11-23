from django.contrib import admin
from .models import MetroLine, MetroStation

@admin.register(MetroLine)
class MetroLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')

@admin.register(MetroStation)
class MetroStationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('lines',)