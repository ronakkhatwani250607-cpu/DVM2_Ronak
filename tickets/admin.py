from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'start_station', 'end_station', 'price', 'status', 'otp_verified', 'created_at')
    list_filter = ('status', 'otp_verified')