from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = ( 
        ("provider", "Provider"), 
        ("finder", "Finder"),
        ("admin","Admin")
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="admin")
    mobile = models.CharField(max_length=15, blank=True, null=True, default="NULL")
    
    def __str__(self): 
        return self.username
