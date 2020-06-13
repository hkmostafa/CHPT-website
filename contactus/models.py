from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
	
	name=models.CharField(max_length=40)
	phone=models.CharField(max_length=10)
	email=models.EmailField(max_length=40)
	subject=models.CharField(max_length=40)
	message=models.TextField()

	def __str__(self):
		return self.subject
