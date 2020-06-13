  
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Appointment,Doctor,Specialty


class RegisterForm(UserCreationForm):
	password1=forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter password'}))
	password2=forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter password confirmation'}))
	#For the registration messages
	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'email' , 'password1', 'password2']:
			self.fields[fieldname].help_text = None

	class Meta:
		model = User
		fields = ['username', 'email']

		widgets = {
		'username' : forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Enter your username',
			}),

		'email' : forms.EmailInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Enter your email',
			}),
		}



class AdminRegisterForm(UserCreationForm):
	password1=forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter password'}))
	password2=forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter password confirmation'}))
	#For the registration messages
	def __init__(self, *args, **kwargs):
		super(AdminRegisterForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'email' , 'password1', 'password2']:
			self.fields[fieldname].help_text = None

	class Meta:
		model = User
		fields = ['username', 'email']

		widgets = {
		'username' : forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Enter username',
			}),

		'email' : forms.EmailInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Enter email',
			}),
		}

class SpecialtyForm(forms.ModelForm):
	class Meta:
		model = Specialty
		fields = ['specialty_name']
		widgets = {

		'specialty_name' : forms.TextInput(
			attrs={
				'class': 'form-control',
			}),
		}




class DoctorForm(forms.ModelForm):
	class Meta:
		model = Doctor
		fields = ['doctor_name','specialty']
		widgets = {

		'doctor_name' : forms.TextInput(
		attrs={
			'class': 'form-control',
			}),

		'specialty' : forms.Select(
			attrs={
				'class': 'form-control',
			}),
		}

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control'}))
	
	def __init__(self, *args, **kwargs):
		super(UserUpdateForm, self).__init__(*args, **kwargs)

		for fieldname in ['username','first_name','last_name','email']:
			self.fields[fieldname].help_text = None

	class Meta:
		model = User
		fields = ['username','first_name','last_name','email', ]

		widgets = {
		'username' : forms.TextInput(
			attrs={
				'class': 'form-control',
			}),
		'first_name' : forms.TextInput(
			attrs={
				'class': 'form-control',
			}),
		'last_name' : forms.TextInput(
			attrs={
				'class': 'form-control',
			}),
		}


class ProfileUpdateForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)

		for fieldname in ['image']:
			self.fields[fieldname].help_text = None

	class Meta:
		model = Profile
		fields = ['image']			
		widgets = {
		'image' : forms.FileInput(
			attrs={
				'class': 'form-control',
			}),

		}





#APPOINTMENT FORMS 



class DateInput(forms.DateInput):
	input_type = 'date'

class RdvForm(forms.ModelForm):

	class Meta:
		model = Appointment 
		fields = [
			'patient_name',
			'patient_cne',
			'patient_email',
			'patient_phone',
			'specialty',
			'doctor',
			'app_date',
			'app_time',
		]

		labels = {
		'patient_name' : 'Patient name' ,
		'patient_cne' : 'CNE number' ,
		'patient_email' : 'Email' ,
		'patient_phone' : 'Phone number' ,
		'specialty' : 'Specialty' ,		
		'doctor' : 'Doctor' ,
		'app_date' : 'Choose appointment date' ,
		'app_time' : 'Choose appointment time' ,



		}
		widgets = {

		'patient_name' : forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Enter full name',
			}),

		'patient_cne' : forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Ex: AA111111',
			}),


		'patient_email' : forms.EmailInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Ex: person@gmail.com',
			}),

		'patient_phone' : forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Enter your phone number',
			}),

		'specialty' : forms.Select(
			attrs={
				'class': 'form-control',
			}),

		'doctor' : forms.Select(
			attrs={
				'class': 'form-control',
			}),
	
		'app_date' : DateInput(
			attrs={
				'class': 'form-control',
			}),

		'app_time' : forms.Select(
			attrs={
				'class': 'form-control',
				'default' : '8:00 - 9:00',
			}),
		}

	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.fields['doctor'].queryset = Doctor.objects.none()	

