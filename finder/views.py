from django.shortcuts import render, redirect
from authentication.models import CustomUser
from provider.models import ParkingSlot
from bookmarks.models import UserParkingBookmark

def finder(request):
    if request.user.is_authenticated:
        user = request.user
        first = user.first_name[0]
        
        # Fetch the user's saved parking slots
        bookmark, created = UserParkingBookmark.objects.get_or_create(user=user)
        saved_slots = bookmark.saved_slots.all()

        # Fetch all parking slots
        parking_slots = ParkingSlot.objects.all()
        
        return render(request, "finder.html", {
            'user': user,
            'first': first,
            'saved_slots': saved_slots,
            'parking_slots': parking_slots
        })
    else:
        return redirect('acc')

def search_parking(request):
    if request.method == "POST":
        user = request.user
        first = user.first_name[0]
        citysearch = request.POST['citysearch']
        parkingspot = ParkingSlot.objects.filter(city__contains=citysearch)
        return render(request, "search.html", {'user': user, 'first': first, 'citysearch': citysearch, 'searchcity': parkingspot})
    
