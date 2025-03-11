from django.db import models
from django.core.validators import RegexValidator

# Public User model
class PublicUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    adhaar = models.CharField(max_length=12, unique=True)
    password = models.CharField(max_length=255)  # Password field to store the hashed password
    is_verified = models.BooleanField(default=False)  # Add a flag to indicate whether OTP is verified

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

# Police Station model
class PoliceStation(models.Model):
    district = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)  # Added email field
    password = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.location}, {self.district}, {self.pincode}"


# Add this to models.py
from django.db import models
from django.utils import timezone
import os

def get_evidence_upload_path(instance, filename):
    # Get the extension of the uploaded file
    ext = filename.split('.')[-1]
    # Create a filename using the user ID and timestamp
    new_filename = f"{instance.user.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    # Return the upload path
    return os.path.join('evidence', new_filename)

class Complaint(models.Model):
    # Complaint status choices
    STATUS_PENDING = 'PENDING'
    STATUS_UNDER_INVESTIGATION = 'UNDER_INVESTIGATION'
    STATUS_RESOLVED = 'RESOLVED'
    STATUS_REJECTED = 'REJECTED'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_UNDER_INVESTIGATION, 'Under Investigation'),
        (STATUS_RESOLVED, 'Resolved'),
        (STATUS_REJECTED, 'Rejected'),
    ]
    
    # Time of day choices
    TIME_MIDNIGHT = 'MIDNIGHT'
    TIME_MORNING = 'MORNING'
    TIME_NOON = 'NOON'
    TIME_AFTERNOON = 'AFTERNOON'
    TIME_EVENING = 'EVENING'
    TIME_NIGHT = 'NIGHT'
    
    TIME_CHOICES = [
        (TIME_MIDNIGHT, 'Midnight (12:00 AM - 12:59 AM)'),
        (TIME_MORNING, 'Morning (6:00 AM - 11:59 AM)'),
        (TIME_NOON, 'Noon (12:00 PM - 12:59 PM)'),
        (TIME_AFTERNOON, 'Afternoon (1:00 PM - 5:59 PM)'),
        (TIME_EVENING, 'Evening (6:00 PM - 8:59 PM)'),
        (TIME_NIGHT, 'Night (9:00 PM - 11:59 PM)'),
    ]
    
    # Complaint type choices
    TYPE_ROBBERY = 'ROBBERY'
    TYPE_ASSAULT = 'ASSAULT'
    TYPE_THREATS = 'THREATS'
    TYPE_BURGLARY = 'BURGLARY'
    TYPE_VANDALISM = 'VANDALISM'
    TYPE_FRAUD = 'FRAUD'
    TYPE_HARASSMENT = 'HARASSMENT'
    TYPE_THEFT = 'THEFT'
    TYPE_DOMESTIC_VIOLENCE = 'DOMESTIC_VIOLENCE'
    TYPE_SEXUAL_ASSAULT = 'SEXUAL_ASSAULT'
    TYPE_KIDNAPPING = 'KIDNAPPING'
    TYPE_STALKING = 'STALKING'
    TYPE_DRUNK_DRIVING = 'DRUNK_DRIVING'
    TYPE_HIT_AND_RUN = 'HIT_AND_RUN'
    TYPE_DRUG_OFFENSES = 'DRUG_OFFENSES'
    TYPE_PUBLIC_INTOXICATION = 'PUBLIC_INTOXICATION'
    TYPE_TRESPASSING = 'TRESPASSING'
    TYPE_HATE_CRIMES = 'HATE_CRIMES'
    TYPE_MURDER = 'MURDER'
    TYPE_ARSON = 'ARSON'
    TYPE_OTHER = 'OTHER'
    
    TYPE_CHOICES = [
        (TYPE_ROBBERY, 'Robbery'),
        (TYPE_ASSAULT, 'Assault'),
        (TYPE_THREATS, 'Threats'),
        (TYPE_BURGLARY, 'Burglary'),
        (TYPE_VANDALISM, 'Vandalism'),
        (TYPE_FRAUD, 'Fraud'),
        (TYPE_HARASSMENT, 'Harassment'),
        (TYPE_THEFT, 'Theft'),
        (TYPE_DOMESTIC_VIOLENCE, 'Domestic Violence'),
        (TYPE_SEXUAL_ASSAULT, 'Sexual Assault'),
        (TYPE_KIDNAPPING, 'Kidnapping'),
        (TYPE_STALKING, 'Stalking'),
        (TYPE_DRUNK_DRIVING, 'Drunk Driving'),
        (TYPE_HIT_AND_RUN, 'Hit and Run'),
        (TYPE_DRUG_OFFENSES, 'Drug Offenses'),
        (TYPE_PUBLIC_INTOXICATION, 'Public Intoxication'),
        (TYPE_TRESPASSING, 'Trespassing'),
        (TYPE_HATE_CRIMES, 'Hate Crimes'),
        (TYPE_MURDER, 'Murder'),
        (TYPE_ARSON, 'Arson'),
        (TYPE_OTHER, 'Other'),
    ]
    
    user = models.ForeignKey(PublicUser, on_delete=models.CASCADE, related_name='complaints')
    police_station = models.ForeignKey(PoliceStation, on_delete=models.CASCADE, related_name='complaints')
    complaint_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField()
    incident_date = models.DateField()
    incident_time = models.CharField(max_length=20, choices=TIME_CHOICES)
    evidence = models.FileField(upload_to=get_evidence_upload_path, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Complaint #{self.id} - {self.get_complaint_type_display()} by {self.user.first_name}"