from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

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

# Police Station model - fixed the duplicate definition
from django.db import models

from django.db import models

class PoliceStation(models.Model):
    district = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)  # Field to track approval

    def __str__(self):
        return f"{self.district} - {self.location}"


from django.db import models
from django.db import models

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under investigation', 'Under Investigation'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),  # Added rejected status
    ]
        
    complaint_type_choices = [
        ('robbery', 'Robbery'),
        ('assault', 'Assault'),
        ('threats', 'Threats'),
        ('burglary', 'Burglary'),
        ('vandalism', 'Vandalism'),
        ('fraud', 'Fraud'),
        ('harassment', 'Harassment'),
        ('theft', 'Theft'),
        ('domestic_violence', 'Domestic Violence'),
        ('sexual_assault', 'Sexual Assault'),
        ('kidnapping', 'Kidnapping'),
        ('stalking', 'Stalking'),
        ('drunk_driving', 'Drunk Driving'),
        ('hit_and_run', 'Hit and Run'),
        ('drug_offenses', 'Drug Offenses'),
        ('public_intoxication', 'Public Intoxication'),
        ('trespassing', 'Trespassing'),
        ('hate_crimes', 'Hate Crimes'),
        ('murder', 'Murder'),
        ('arson', 'Arson'),
        ('other', 'Other')
    ]
        
    time_choices = [
        ('midnight', '12:00 AM - 12:59 AM'),
        ('morning', '6:00 AM - 11:59 AM'),
        ('noon', '12:00 PM - 12:59 PM'),
        ('afternoon', '1:00 PM - 5:59 PM'),
        ('evening', '6:00 PM - 8:59 PM'),
        ('night', '9:00 PM - 11:59 PM'),
    ]
    
    # ForeignKey fields - changed to point to the same PoliceStation model
    district = models.ForeignKey(PoliceStation, related_name='district_complaints', on_delete=models.CASCADE)
    location = models.ForeignKey(PoliceStation, related_name='location_complaints', on_delete=models.CASCADE)
    complaint_type = models.CharField(max_length=50, choices=complaint_type_choices)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    evidence = models.FileField(upload_to='evidence/', blank=True, null=True)
        
    # Fixed the date field to properly handle dates
    incident_date = models.DateField(help_text="Format: YYYY-MM-DD")
    
    # Automatically set field to capture the date and time when the form is submitted
    submission_timestamp = models.DateTimeField(default=timezone.now)
    
    time_of_incident = models.CharField(max_length=20, choices=time_choices)
    
    def __str__(self):
        return f"{self.district} - {self.location} - {self.complaint_type}"


