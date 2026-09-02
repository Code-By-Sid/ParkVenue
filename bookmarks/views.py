from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import CustomUser
from provider.models import ParkingSlot
from .models import UserParkingBookmark

def savedparking(request):
    if request.user.is_authenticated:
        user = request.user
        first = user.first_name[0]
        bookmark, created = UserParkingBookmark.objects.get_or_create(user=request.user)
        slots = bookmark.saved_slots.all()
        return render(request, "savedparking.html", {'user': user, 'first': first, "slots": slots})
    else:
        return redirect('acc')

def toggle_bookmark(request, slot_id):
    slot = get_object_or_404(ParkingSlot, id=slot_id)
    bookmark, created = UserParkingBookmark.objects.get_or_create(user=request.user)

    if slot in bookmark.saved_slots.all():
        bookmark.saved_slots.remove(slot)
    else:
        bookmark.saved_slots.add(slot)

    return redirect('savedparking')
    
