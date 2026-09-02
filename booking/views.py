from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import CustomUser
from provider.models import ParkingSlot
from .models import Reservation

def reserve_spot(request, spot_id):
    parking_spot = get_object_or_404(ParkingSlot, id=spot_id)

    # Check if slots are available
    if parking_spot.no_of_slots > 0:
        # Create a reservation entry
        Reservation.objects.create(user=request.user, parking_spot=parking_spot)

        # Reduce the available slots count
        parking_spot.no_of_slots -= 1
        parking_spot.save()
        
        return redirect('findreservation')
    else:
        return render(request, "reservation_failed.html", {"message": "No slots available!"})

def finderreservation(request):
    if request.user.is_authenticated:
        user = request.user
        first = user.first_name[0]
        reservations = Reservation.objects.filter(user=request.user, status="pending").order_by('-start_time')
        accepted_reservations = Reservation.objects.filter(user=user, status="confirmed").order_by('-start_time')
        return render(request, "finderreservation.html", {'user': user, 'first': first, 'reservations': reservations, 'accepted_reservations': accepted_reservations})
    else:
        return redirect('acc')

def cancel_parking(request, reservation_id):
    if request.user.is_authenticated:
        reserve = get_object_or_404(Reservation, id=reservation_id, user=request.user)
        reserve.delete()
        return redirect('findreservation')
    else:
        return redirect('acc')
    
