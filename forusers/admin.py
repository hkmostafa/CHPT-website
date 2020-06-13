from django.contrib import admin
from .models import Profile,Appointment,Doctor,Specialty
# Register your models here.
admin.site.register(Profile)
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Specialty)