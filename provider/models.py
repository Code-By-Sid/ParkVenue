from django.db import models
from authentication.models import CustomUser

class ParkingSlot(models.Model):
    name = models.CharField(max_length=10, unique=True)
    no_of_slots = models.IntegerField(default=0)
    city = models.CharField(max_length=30, default="India")
    latitude = models.FloatField()
    longitude = models.FloatField()
    available_slots = models.IntegerField(default=0)
    opening_time = models.TimeField(default="08:00:00")
    closing_time = models.TimeField(default="22:00:00")
    SECURITY_CHOICES = [
        ('basic', 'Basic (Lighting)'),
        ('standard', 'Standard (CCTV)'),
        ('premium', 'Premium (24/7 Security)'),
    ]
    security_level = models.CharField(max_length=10, choices=SECURITY_CHOICES, default="basic")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="parking_slots")

    def __str__(self):
        return f"{self.name} - {self.available_slots} slots available"
