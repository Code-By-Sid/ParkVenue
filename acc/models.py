from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    ROLE_CHOICES = ( 
    ("provider", "Provider"), 
    ("finder", "Finder"),
    ("admin","Admin"))
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default="admin")
    mobile = models.CharField(max_length=15, blank=True, null=True,default="NULL")
    def __str__(self): 
        return self.username
    
class ParkingSlot(models.Model):
    name = models.CharField(max_length=10, unique=True)
    no_of_slots = models.IntegerField(default=0)  # Changed to IntegerField
    city = models.CharField(max_length=30,default="India")
    latitude = models.FloatField()
    longitude = models.FloatField()
    available_slots = models.IntegerField(default=0)  # Changed to IntegerField
    opening_time = models.TimeField(default="08:00:00")
    closing_time = models.TimeField(default="22:00:00")
    SECURITY_CHOICES = [
        ('basic', 'Basic (Lighting)'),
        ('standard', 'Standard (CCTV)'),
        ('premium', 'Premium (24/7 Security)'),
    ]
    security_level = models.CharField(max_length=10, choices=SECURITY_CHOICES,default="basic")
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="parking_slots")

    def __str__(self):
        return f"{self.name} - {self.available_slots} slots available"

class Reservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parking_spot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)  # Reservation start time
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("confirmed", "Confirmed")],
        default="pending"
    )

    def __str__(self):
        return f"Reservation by {self.user.username} at {self.parking_spot.name} - {self.status}"
    
class UserParkingBookmark(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='bookmarks')
    saved_slots = models.ManyToManyField(ParkingSlot, blank=True)

    def __str__(self):
        return f"Bookmarks of {self.user.username}"
