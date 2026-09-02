from django.db import models
from authentication.models import CustomUser
from provider.models import ParkingSlot

class Reservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parking_spot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("confirmed", "Confirmed")],
        default="pending"
    )

    def __str__(self):
        return f"Reservation by {self.user.username} at {self.parking_spot.name} - {self.status}"
