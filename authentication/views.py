from django.shortcuts import render, redirect
from .util import send_email_to, send_email_reset
from django.contrib.auth.models import auth
from django.contrib.auth import logout as logouts
from .models import CustomUser
from django.contrib import messages
from django.http import HttpResponse

def initial(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "index.html")

def choice(request):
    if request.method == "POST":
        role = request.POST.get("role")
        if role in ["provider", "finder"]:
            request.session["user_role"] = role
            return redirect('otp')
    return render(request, "choice.html")
    
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                if request.user.role == "provider":
                    return redirect('home')
                else:
                    return redirect('finder')
            
            # Check if the user already exists
            if CustomUser.objects.filter(email=username).exists():
                error = "Invalid credentials. Please try again."
                return render(request, 'account.html', {'error': error})
            else:
                error = "You don't have account. Please create one."
                return render(request, "account.html", {'error': error})
                
    return render(request, "account.html")

def createaccount(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method == "POST":
            request.session['id'] = 0
            first_name = request.POST['first_name']
            request.session['first_name'] = first_name
            last_name = request.POST['last_name']
            request.session['last_name'] = last_name
            email = request.POST['email']
            request.session['email'] = email
            request.session['password'] = request.POST['password']
            
            # Check if the user already exists
            if CustomUser.objects.filter(email=email).exists():
                error = "An account with this email already exists. Please log in."
                return render(request, "createaccount.html", {'error': error})
            else:
                otp = send_email_to(email, first_name, last_name)
                request.session['otp'] = otp
                return redirect('choice')

    return render(request, "createaccount.html")

def forgot(request):
    if request.method == "POST":
        email = request.POST['email']
        request.session['email'] = email

        # Check if the user already exists
        if CustomUser.objects.filter(email=email).exists():
            request.session['id'] = 1
            otp = send_email_reset(email)
            request.session['otp'] = otp
            return redirect('otp')
        else:
            error = "You don't have account. Please create one."
            return render(request, "forgot.html", {'error': error})
            
    return render(request, "forgot.html")

def otp(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.session['id'] == 0:
            first_name = request.session['first_name']
            last_name = request.session['last_name']
            email = request.session['email']
            password = request.session['password']
            otp = request.session['otp']
            role = request.session['user_role']
            print(otp)

            if request.method == "POST":
                userotp = int(request.POST['otp'])
                print(userotp)

                if otp == userotp:
                    data = CustomUser.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        username=email,
                        password=password,
                        role=role
                    )
                    return redirect('acc')
                else:
                    error = "Invalid OTP . Please try again"
                    return render(request, "otp.html", {"error": error})
                
        elif request.session['id'] == 1:
            otp = request.session['otp']
            
            if request.method == "POST":
                userotp = int(request.POST['otp'])

                if otp == userotp:
                    return redirect('resetpass')
                else:
                    error = "Invalid OTP . Please try again"
                    return render(request, "otp.html", {"error": error})

    return render(request, "otp.html")

def logout(request):
    if request.method == 'POST':
        logouts(request)
        return redirect('acc')

def resetpass(request):
    if request.method == "POST":
        password = request.POST['password']
        email = request.session['email']
        u = CustomUser.objects.get(email=email)
        u.set_password(password)
        u.save()
        return redirect('acc')
    
    return render(request, 'resetpass.html')
