from django.db import models
from authentication.models import CustomUser
from provider.models import ParkingSlot

class UserParkingBookmark(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='bookmarks')
    saved_slots = models.ManyToManyField(ParkingSlot, blank=True)

    def __str__(self):
        return f"Bookmarks of {self.user.username}"
