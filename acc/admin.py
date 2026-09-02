from django.contrib import admin
from .models import CustomUser,ParkingSlot,UserParkingBookmark,Reservation
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ParkingSlot)
admin.site.register(UserParkingBookmark)
admin.site.register(Reservation)
