from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from authentication.models import CustomUser
from .models import ParkingSlot
from booking.models import Reservation

def home(request):
    if request.user.is_authenticated:
        user = request.user
        first = user.first_name[0]
        return render(request, "pro_dashboard.html", {'user': user, 'first': first})
    else:
        return redirect('acc')

def proinfo(request):
    if request.user.is_authenticated:
        user = request.user
        first = user.first_name[0]
        
        # Count available parking spots for the logged-in user
        count = ParkingSlot.objects.filter(user=user).count()

        return render(request, "providerinfo.html", {
            'user': user,
            'first': first,
            'count': count
        })
    else:
        return redirect('acc')

def proeditinfo(request):
    if request.user.is_authenticated:
        user = request.user  # Get the logged-in user
        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            # Update user details
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.mobile = phone
            
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("proeditinfo")
        
        user = request.user
        first = user.first_name[0]
        return render(request, "proedit_info.html", {'user': user, 'first': first})
    else:
        return redirect('acc')

def addspot(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get("spot_name")
            latitude = request.POST.get("latitude")
            longitude = request.POST.get("longitude")
            price_per_hour = request.POST.get("price_per_hour")
            opening_time = request.POST.get("opening_time")
            closing_time = request.POST.get("closing_time")
            security_level = request.POST.get("security")
            total_slots = request.POST.get("total_slots")
            city = request.POST.get("city")
            # Create a new parking spot
            ParkingSlot.objects.create(
                user=request.user,
                name=name,
                latitude=latitude,
                longitude=longitude,
                price=price_per_hour,
                opening_time=opening_time,
                closing_time=closing_time,
                available_slots=total_slots,
                no_of_slots=total_slots,
                security_level=security_level,
                city=city
            )
            return redirect('managepark')
        user = request.user
        first = user.first_name[0]
        return render(request, "addspot.html", {'user': user, 'first': first})
    else:
        return redirect('acc')

def managepark(request):
    if request.user.is_authenticated:
        user = request.user
        first = user.first_name[0]

        # Fetch parking spots added by the logged-in user
        user_parking_spots = ParkingSlot.objects.filter(user=user)

        return render(request, "managepaking.html", {'user': user, 'first': first, 'parking_spots': user_parking_spots})
    else:
        return redirect('acc')

def delete_parking(request, spot_id):
    if request.user.is_authenticated:
        spot = get_object_or_404(ParkingSlot, id=spot_id, user=request.user)
        spot.delete()
        return redirect('managepark')
    else:
        return redirect('acc')
    
def reservation(request):
    if request.user.is_authenticated:
        user = request.user
        first = user.first_name[0]

        # Fetch reservations for the parking spots owned by the user
        user_parking_spots = ParkingSlot.objects.filter(user=user)
        reservations = Reservation.objects.filter(parking_spot__in=user_parking_spots, status="pending")
        
        # Fetch confirmed reservations related to these parking slots
        confirmed_reservations = Reservation.objects.filter(
            parking_spot__in=user_parking_spots, status="confirmed"
        )
        return render(request, "providerreservation.html", {
            'user': user,
            'first': first,
            'reservations': reservations,
            "confirmed_reservations": confirmed_reservations,
        })
    else:
        return redirect('acc')
    
def update_reservation(request, reservation_id):
    if request.method == "POST":
        reservation = get_object_or_404(Reservation, id=reservation_id)
        parking_spot = reservation.parking_spot

        action = request.POST.get("action")
        if action == "approve":
            if parking_spot.available_slots > 0:
                reservation.status = "confirmed"
                parking_spot.available_slots -= 1
                reservation.save()
                parking_spot.save()
            else:
                return redirect('reservation')

        elif action == "decline":
            reservation.delete()

        return redirect('reservation')

    return redirect('reservation')

def delete_reservation(request, reservation_id):
    if request.method == "POST":
        reservation = get_object_or_404(Reservation, id=reservation_id)
        parking_spot = reservation.parking_spot
        
        # Increase available slots when reservation is deleted
        parking_spot.available_slots += 1  
        parking_spot.save()

        # Delete the reservation
        reservation.delete()

        return redirect('reservation')
    
