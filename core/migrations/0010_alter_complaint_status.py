# Generated by Django 5.1.7 on 2025-03-08 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_policestation_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('under investigation', 'Under Investigation'), ('resolved', 'Resolved'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
    ]
