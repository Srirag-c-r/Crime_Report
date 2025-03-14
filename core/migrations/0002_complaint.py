# Generated by Django 5.1.7 on 2025-03-11 05:52

import core.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint_type', models.CharField(choices=[('ROBBERY', 'Robbery'), ('ASSAULT', 'Assault'), ('THREATS', 'Threats'), ('BURGLARY', 'Burglary'), ('VANDALISM', 'Vandalism'), ('FRAUD', 'Fraud'), ('HARASSMENT', 'Harassment'), ('THEFT', 'Theft'), ('DOMESTIC_VIOLENCE', 'Domestic Violence'), ('SEXUAL_ASSAULT', 'Sexual Assault'), ('KIDNAPPING', 'Kidnapping'), ('STALKING', 'Stalking'), ('DRUNK_DRIVING', 'Drunk Driving'), ('HIT_AND_RUN', 'Hit and Run'), ('DRUG_OFFENSES', 'Drug Offenses'), ('PUBLIC_INTOXICATION', 'Public Intoxication'), ('TRESPASSING', 'Trespassing'), ('HATE_CRIMES', 'Hate Crimes'), ('MURDER', 'Murder'), ('ARSON', 'Arson'), ('OTHER', 'Other')], max_length=50)),
                ('description', models.TextField()),
                ('incident_date', models.DateField()),
                ('incident_time', models.CharField(choices=[('MIDNIGHT', 'Midnight (12:00 AM - 12:59 AM)'), ('MORNING', 'Morning (6:00 AM - 11:59 AM)'), ('NOON', 'Noon (12:00 PM - 12:59 PM)'), ('AFTERNOON', 'Afternoon (1:00 PM - 5:59 PM)'), ('EVENING', 'Evening (6:00 PM - 8:59 PM)'), ('NIGHT', 'Night (9:00 PM - 11:59 PM)')], max_length=20)),
                ('evidence', models.FileField(blank=True, null=True, upload_to=core.models.get_evidence_upload_path)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('UNDER_INVESTIGATION', 'Under Investigation'), ('RESOLVED', 'Resolved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('police_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='core.policestation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='core.publicuser')),
            ],
        ),
    ]
