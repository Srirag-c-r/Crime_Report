from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PublicUser, PoliceStation, Complaint

admin.site.register(PublicUser)
admin.site.register(PoliceStation)
admin.site.register(Complaint)