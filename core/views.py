from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from .models import PublicUser, PoliceStation, Complaint
import random
import string


# Generate a random OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


# Register Page View
def register(request):
    return render(request, 'register.html')


# Home Page View
def home(request):
    return render(request, 'home.html')


# About Page View
def about(request):
    return render(request, 'about.html')


# Public User Registration View
def public_user_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        adhaar = request.POST.get('adhaar')
        password = request.POST.get('password')

        # Hash the password before saving
        hashed_password = make_password(password)

        # Creating and saving the PublicUser instance with hashed password
        user = PublicUser(first_name=first_name, last_name=last_name, phone=phone, email=email, adhaar=adhaar, password=hashed_password)
        user.save()

        # Generate OTP
        otp = generate_otp()

        # Send OTP to the user's email
        send_mail(
            'OTP Verification for Safe Call',
            f'Your OTP for Safe Call registration is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        # Store OTP in session for later verification
        request.session['otp'] = otp
        request.session['public_user_id'] = user.id

        messages.success(request, 'You have successfully registered. Please check your email for the OTP verification.')
        return redirect('verify_otp')
    return render(request, 'register.html', {'is_public_user': True})


# OTP Verification for Public User
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == request.session.get('otp'):
            # OTP is valid, mark the user as verified
            user = PublicUser.objects.get(id=request.session.get('public_user_id'))
            user.is_verified = True
            user.save()

            messages.success(request, 'Your OTP has been verified successfully. You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'verify_otp.html')


# Police Station Registration View
# Police Station Registration View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import PoliceStation

# Police Station Registration View
def police_station_registration(request):
    if request.method == 'POST':
        district = request.POST.get('district')
        location = request.POST.get('location')
        pincode = request.POST.get('pincode')
        contact = request.POST.get('contact')
        email = request.POST.get('email')  # Get email from form
        password = request.POST.get('password')

        # Hash the password before saving
        hashed_password = make_password(password)

        # Save the police station record
        police_station = PoliceStation(
            district=district,
            location=location,
            pincode=pincode,
            contact=contact,
            email=email,  # Save email
            password=hashed_password
        )
        police_station.save()

        messages.success(request, 'Your police station has been registered. It will be approved by the admin soon.')
        return redirect('home')

    return render(request, 'register.html', {'is_police_station': True})



# Login View (General login page)
def login_view(request):
    if request.method == 'POST':
        login_type = request.POST.get('login_as')
        
        # Redirect to respective login page
        if login_type == 'user':
            return redirect('user_login')
        elif login_type == 'police_station':
            return redirect('police_station_login')
        
    return render(request, 'login.html')


# User Login
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = PublicUser.objects.get(email=email)  # Fetch user by email
            if check_password(password, user.password):  # Verify password
                request.session['user_id'] = user.id  # Store user ID in session
                request.session['user_name'] = f"{user.first_name} {user.last_name}"  # Store full name
                
                messages.success(request, 'Login successful.')
                return redirect('user_dashboard')  # Redirect to user dashboard
            else:
                messages.error(request, 'Invalid login credentials. Please try again.')
        except PublicUser.DoesNotExist:
            messages.error(request, 'Invalid login credentials. Please try again.')

    return render(request, 'user_login.html')


# Police Station Login
def police_station_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Fetch the police station by email
            police_station = PoliceStation.objects.get(email=email)

            # Check if the password is correct
            if check_password(password, police_station.password):
                # Check if the police station is approved
                if police_station.is_approved:
                    # Store necessary session data
                    request.session['police_station_id'] = police_station.id
                    request.session['police_station_branch'] = f"{police_station.district} - {police_station.location}"
                    
                    messages.success(request, 'Login successful as Police Station.')
                    return redirect('police_station_dashboard')
                else:
                    # If not approved, show an error message
                    messages.error(request, 'Your police station account is not approved yet. Please contact the admin.')
            else:
                messages.error(request, 'Invalid login credentials. Please try again.')

        except PoliceStation.DoesNotExist:
            messages.error(request, 'Invalid login credentials. Please try again.')

    return render(request, 'police_station_login.html')


# User Dashboard View
def user_dashboard(request):
    return render(request, 'user_dashboard.html')


# Police Station Dashboard View
def police_station_dashboard(request):
    return render(request, 'police_station_dashboard.html')


# User Logout
def user_logout(request):
    request.session.flush()  # Clears session
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


# Police Station Logout
def police_station_logout(request):
    request.session.flush()  # Clears session
    messages.success(request, "You have successfully logged out as Police Station.")
    return redirect('login')


# Add Complaint View - Fixed with improved error handling
def add_complaint(request):
    if request.method == 'POST':
        try:
            district_id = request.POST['district']
            location_id = request.POST['location']
            complaint_type = request.POST['complaint_type']
            description = request.POST['description']
            evidence = request.FILES.get('evidence')  # optional file upload
            incident_date = request.POST['incident_date']
            time_of_incident = request.POST['time_of_incident']

            # Validate date format
            try:
                # Try to parse the date to ensure it's in YYYY-MM-DD format
                from datetime import datetime
                parsed_date = datetime.strptime(incident_date, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD format.')
                police_stations = PoliceStation.objects.all()
                return render(request, 'add_complaint.html', {'police_stations': police_stations})

            # Get the related PoliceStation instances
            district = PoliceStation.objects.get(id=district_id)
            location = PoliceStation.objects.get(id=location_id)

            # Create a new Complaint object and save it
            complaint = Complaint.objects.create(
                district=district,
                location=location,
                complaint_type=complaint_type,
                description=description,
                evidence=evidence,
                incident_date=parsed_date,
                time_of_incident=time_of_incident,
                submission_timestamp=timezone.now()
            )

            messages.success(request, 'Complaint submitted successfully!')
            return redirect('user_dashboard')  # Redirect to a page showing all complaints
        
        except Exception as e:
            messages.error(request, f'Error submitting complaint: {str(e)}')
    
    # Fetch all PoliceStation objects to populate the dropdowns
    police_stations = PoliceStation.objects.all()
    return render(request, 'add_complaint.html', {'police_stations': police_stations})


# View to list complaints
def complaint_list(request):
    complaints = Complaint.objects.all().order_by('-submission_timestamp')
    return render(request, 'complaint_list.html', {'complaints': complaints})