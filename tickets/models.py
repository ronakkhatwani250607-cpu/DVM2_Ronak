from django.db import models
from django.contrib.auth import get_user_model
from metro.models import MetroStation, MetroLine
from django.utils import timezone

User = get_user_model()

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('in_use', 'In Use'),
    ]
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    start_station = models.ForeignKey(MetroStation, on_delete=models.CASCADE, related_name='start_tickets')
    end_station = models.ForeignKey(MetroStation, on_delete=models.CASCADE, related_name='end_tickets')
    line = models.ForeignKey(MetroLine, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    otp_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.passenger.email or self.passenger.username}: {self.start_station} -> {self.end_station}"