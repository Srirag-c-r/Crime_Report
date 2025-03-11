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
# Police Station Login
def police_station_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            police_station = PoliceStation.objects.get(email=email)  # Lookup using email
            
            # Check if the police station is approved
            if not police_station.approved:
                messages.error(request, 'Your account has not been approved by the admin yet.')
                return redirect('police_station_login')

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
    return redirect('login')  # Redirect to login page or a suitable page


# Add these imports at the top of your views.py
from django.http import JsonResponse
from .models import PublicUser, PoliceStation, Complaint
from django.utils import timezone
from django.core.files.storage import default_storage
import json

# Add Complaint View
def add_complaint(request):
    # Check if user is logged in
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to register a complaint.")
        return redirect('login')
        
    # Get the user
    try:
        user = PublicUser.objects.get(id=request.session['user_id'])
    except PublicUser.DoesNotExist:
        messages.error(request, "User account not found.")
        return redirect('login')
    
    if request.method == 'POST':
        # Get form data
        police_station_id = request.POST.get('police_station')
        complaint_type = request.POST.get('complaint_type')
        description = request.POST.get('description')
        incident_date = request.POST.get('incident_date')
        incident_time = request.POST.get('incident_time')
        
        # Validate required fields
        if not all([police_station_id, complaint_type, description, incident_date, incident_time]):
            messages.error(request, "All fields are required except evidence.")
            return redirect('add_complaint')
        
        try:
            # Get the police station
            police_station = PoliceStation.objects.get(id=police_station_id)
            
            # Create complaint object
            complaint = Complaint(
                user=user,
                police_station=police_station,
                complaint_type=complaint_type,
                description=description,
                incident_date=incident_date,
                incident_time=incident_time,
                status=Complaint.STATUS_PENDING,
            )
            
            # Handle evidence file if provided
            if 'evidence' in request.FILES:
                evidence_file = request.FILES['evidence']
                complaint.evidence = evidence_file
            
            # Save the complaint
            complaint.save()
            
            messages.success(request, "Your complaint has been registered successfully. The reference number is #" + str(complaint.id))
            return redirect('view_complaints')
            
        except PoliceStation.DoesNotExist:
            messages.error(request, "Selected police station not found.")
            return redirect('add_complaint')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_complaint')
    
    # For GET request, prepare data for the form
    # Get districts for dropdown
    districts = PoliceStation.objects.values_list('district', flat=True).distinct()
    
    # Initial context without locations
    context = {
        'districts': districts,
        'complaint_types': Complaint.TYPE_CHOICES,
        'time_choices': Complaint.TIME_CHOICES
    }
    
    return render(request, 'add_complaint.html', context)

# Get locations for a district (AJAX endpoint)
def get_locations(request):
    if request.method == 'GET':
        district = request.GET.get('district')
        if district:
            locations = PoliceStation.objects.filter(district=district).values('id', 'location')
            return JsonResponse(list(locations), safe=False)
    return JsonResponse([], safe=False)

# View User Complaints
def view_complaints(request):
    # Check if user is logged in
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view complaints.")
        return redirect('login')
        
    # Get the user
    try:
        user = PublicUser.objects.get(id=request.session['user_id'])
        # Get all complaints for this user
        complaints = Complaint.objects.filter(user=user).order_by('-created_at')
        return render(request, 'view_complaints.html', {'complaints': complaints})
    except PublicUser.DoesNotExist:
        messages.error(request, "User account not found.")
        return redirect('login')
