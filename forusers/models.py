from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


# PROFILE MODEL

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pics', blank=True)
	def __str__(self):
		return self.user.username+"' profile"

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)	


#APPOINTMENT MODELS

time_choices = [
	('8:00 - 9:00', '8:00 - 9:00'),
	('9:00 - 10:00', '9:00 - 10:00'),
	('10:00 - 11:00', '10:00 - 11:00'),
	('11:00 - 12:00', '11:00 - 12:00'),
	('14:00 - 15:00', '14:00 - 15:00'),
	('15:00 - 16:00', '15:00 - 16:00'),
	('16:00 - 17:00', '16:00 - 17:00'),
	('17:00 - 18:00', '17:00 - 18:00'),

]
#Specialty Class
class Specialty(models.Model):
	specialty_name=models.CharField(max_length=40)
	
	def __str__(self):
		return self.specialty_name


#Doctor Class
class Doctor(models.Model):
	doctor_name=models.CharField(max_length=50)
	specialty=models.ForeignKey(Specialty, on_delete=models.CASCADE)

	def __str__(self):
		return self.doctor_name


#Appointment Class
class Appointment(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	patient_name=models.CharField(max_length=40)
	patient_cne=models.CharField(max_length=8)
	patient_email=models.EmailField(max_length=40)
	patient_phone=models.CharField(max_length=10)
	specialty=models.ForeignKey(Specialty, on_delete=models.CASCADE)
	doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
	app_date=models.DateField(default=timezone.now)
	app_time=models.CharField(max_length=30,choices=time_choices)

	def __str__(self):
		return self.patient_name+"'s appointment"
