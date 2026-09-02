from django.shortcuts import render,redirect,get_object_or_404
from .util import send_email_to,send_email_reset
from django.contrib.auth.models import auth
from . models import CustomUser,UserParkingBookmark,ParkingSlot,Reservation
from django.contrib import messages
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import logout as logouts
from django.http import JsonResponse

def initial(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,"index.html")

def choice(request):
    if request.method == "POST":
        role = request.POST.get("role")
        if role in ["provider", "finder"]:
            request.session["user_role"] = role
            return redirect('otp')

    return render(request,"choice.html")
    
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=="POST":
            username = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request,user)
                if request.user.role=="provider":
                    return redirect('home')
                else:
                    return redirect('finder')
            
            # Check if the user already exists
            if CustomUser.objects.filter(email=username).exists():
                error="Invalid credentials. Please try again."
                return render(request,'account.html',{'error':error})
            else:
                error="You don't have account. Please create one."
                return render(request,"account.html",{'error':error})
                
    return render(request,"account.html")

def createaccount(request):

    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method=="POST":
            request.session['id']=0
            first_name= request.POST['first_name']
            request.session['first_name'] = first_name
            last_name= request.POST['last_name']
            request.session['last_name']=last_name
            email = request.POST['email']
            request.session['email'] = email
            request.session['password'] = request.POST['password']
            
            # Check if the user already exists
            if CustomUser.objects.filter(email=email).exists():
                error="An account with this email already exists. Please log in."
                return render(request,"createaccount.html",{'error':error})
            else:
                otp = send_email_to(email,first_name,last_name)
                request.session['otp']= otp
                return redirect('choice')

    return render(request,"createaccount.html")

def forgot(request):
    if request.method=="POST":

        email = request.POST['email']
        request.session['email']=email

        # Check if the user already exists
        if CustomUser.objects.filter(email=email).exists():
            request.session['id']=1
            otp = send_email_reset(email)
            request.session['otp']=otp
            return redirect('otp')

        else:
            error="You don't have account. Please create one."
            return render(request,"forgot.html",{'error':error})
            
    return render(request,"forgot.html")

def otp(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.session['id']==0:
            first_name=request.session['first_name']
            last_name=request.session['last_name']
            email=request.session['email']
            password=request.session['password']
            otp= request.session['otp']
            role = request.session['user_role']
            print(otp)

            if request.method=="POST":
                userotp = int(request.POST['otp'])
                print(userotp)

                if otp==userotp:
                    data= CustomUser.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=email,password=password,role=role)
                    return redirect('acc')

                else:
                    error="Invalid OTP . Please try again"
                    return render(request,"otp.html",{"error":error})
                
        elif request.session['id']==1:

            otp = request.session['otp']
            
            if request.method=="POST":

                userotp= int(request.POST['otp'])

                if otp==userotp:
                    return redirect('resetpass')
                else:
                    error="Invalid OTP . Please try again"
                    return render(request,"otp.html",{"error":error})

    return render(request,"otp.html")

def logout(request):
    if request.method=='POST':
        logouts(request)
        return redirect('acc')

def resetpass(request):

    if request.method=="POST":
        
        password= request.POST['password']
        email = request.session['email']
        u = CustomUser.objects.get(email=email)
        u.set_password(password)
        u.save()
        return redirect('acc')
    
    return render(request,'resetpass.html')

def home(request):
    if request.user.is_authenticated:
        user = request.user
        first = user.first_name[0]
        return render(request,"pro_dashboard.html",{'user': user,'first': first})
    else:
        return redirect('acc')  # Redirect to login if not authenticated

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
        return redirect('acc')  # Redirect to login if not authenticated

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
            user.mobile = phone  # Assuming 'phone' is stored in a Profile model
            
            user.save()  # Save the updated user data
            messages.success(request, "Profile updated successfully!")
            return redirect("proeditinfo")  # Redirect to the same page after saving
        
        user = request.user
        first = user.first_name[0]
        return render(request,"proedit_info.html",{'user': user,'first': first})
    else:
        return redirect('acc')  # Redirect to login if not authenticated

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
                    available_slots= total_slots,
                    no_of_slots= total_slots,
                    security_level=security_level,
                    city=city)
                return redirect('managepark')
            user = request.user
            first = user.first_name[0]
            return render(request,"addspot.html",{'user': user,'first': first})
    else:
        return redirect('acc')  # Redirect to login if not authenticated

def managepark(request): 
    if request.user.is_authenticated:
        user = request.user
        first = user.first_name[0]

        # Fetch parking spots added by the logged-in user
        user_parking_spots = ParkingSlot.objects.filter(user=user)  

        return render(request, "managepaking.html", {'user': user, 'first': first, 'parking_spots': user_parking_spots})
    else:
        return redirect('acc')  # Redirect to login if not authenticated

def delete_parking(request, spot_id):
    if request.user.is_authenticated:
        spot = get_object_or_404(ParkingSlot, id=spot_id, user=request.user)
        spot.delete()
        return redirect('managepark')  # Redirect back to parking management page
    else:
        return redirect('acc')  # Redirect to login if not authenticated
    
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
        return redirect('acc')  # Redirect to login if not authenticated
    
def update_reservation(request, reservation_id):
    if request.method == "POST":
        reservation = get_object_or_404(Reservation, id=reservation_id)
        parking_spot = reservation.parking_spot  # Get the related parking spot

        action = request.POST.get("action")
        if action == "approve":
            if parking_spot.available_slots > 0:  # Ensure slots are available
                reservation.status = "confirmed"
                parking_spot.available_slots -= 1  # Reduce available slots
                reservation.save()
                parking_spot.save()
            else:
                # Optional: Show a message if no slots are available
                return redirect('reservation')

        elif action == "decline":
            reservation.delete()

        return redirect('reservation')  # Redirect back to reservation list

    return redirect('reservation')  # Redirect if method is not POST

def delete_reservation(request, reservation_id):
    if request.method == "POST":
        reservation = get_object_or_404(Reservation, id=reservation_id)
        parking_spot = reservation.parking_spot  # Get related parking spot
        
        # Increase available slots when reservation is deleted
        parking_spot.available_slots += 1  
        parking_spot.save()

        # Delete the reservation
        reservation.delete()

        return redirect('reservation')  # Redirect to the list
    
def reserve_spot(request, spot_id):
    parking_spot = get_object_or_404(ParkingSlot, id=spot_id)

    # Check if slots are available
    if parking_spot.no_of_slots > 0:
        # Create a reservation entry
        Reservation.objects.create(user=request.user, parking_spot=parking_spot)

        # Reduce the available slots count
        parking_spot.no_of_slots -= 1
        parking_spot.save()
        
        return redirect('findreservation')  # Redirect after reservation
    else:
        return render(request, "reservation_failed.html", {"message": "No slots available!"})
    
def finder(request):
    if request.user.is_authenticated:
        user = request.user
        first = user.first_name[0]
        
        # Fetch the user's saved parking slots
        bookmark, created = UserParkingBookmark.objects.get_or_create(user=user)
        saved_slots = bookmark.saved_slots.all()

        # Fetch all parking slots (or any other data you need to display)
        parking_slots = ParkingSlot.objects.all()
        
        return render(request, "finder.html", {
            'user': user,
            'first': first,
            'saved_slots': saved_slots,
            'parking_slots': parking_slots
        })
    else:
        return redirect('acc')  # Redirect to login if not authenticated
       
def savedparking(request):
        if request.user.is_authenticated:
            user = request.user
            first = user.first_name[0]
            bookmark, created = UserParkingBookmark.objects.get_or_create(user=request.user)
            slots = bookmark.saved_slots.all()
            return render(request,"savedparking.html",{'user': user,'first':first,"slots": slots})
        else:
            return redirect('acc')

def toggle_bookmark(request, slot_id):
    slot = get_object_or_404(ParkingSlot, id=slot_id)
    bookmark, created = UserParkingBookmark.objects.get_or_create(user=request.user)

    if slot in bookmark.saved_slots.all():
        bookmark.saved_slots.remove(slot)  # Unsave the slot
    else:
        bookmark.saved_slots.add(slot)  # Save the slot

    return redirect('savedparking')  # Redirect back to saved slots page

def finderreservation(request):
        if request.user.is_authenticated:
            user = request.user
            first = user.first_name[0]
            reservations = Reservation.objects.filter(user=request.user, status="pending").order_by('-start_time')
            accepted_reservations = Reservation.objects.filter(user=user,status="confirmed").order_by('-start_time')
            return render(request,"finderreservation.html",{'user': user,'first':first,'reservations': reservations,'accepted_reservations':accepted_reservations})
        else:
            return redirect('acc')

def cancel_parking(request, reservation_id):
    if request.user.is_authenticated:
        reserve = get_object_or_404(Reservation, id=reservation_id, user=request.user)
        reserve.delete()
        return redirect('findreservation')  # Redirect back to parking management page
    else:
        return redirect('acc')  # Redirect to login if not authenticated


def search_parking(request):
    if request.method =="POST":
        user = request.user
        first = user.first_name[0]
        citysearch = request.POST['citysearch']
        parkingspot = ParkingSlot.objects.filter(city__contains=citysearch)
        return render(request,"search.html",{'user': user,'first':first,'citysearch':citysearch,'searchcity':parkingspot})
    