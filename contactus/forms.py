from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
	
	class Meta:
		model = Contact 
		fields = [
			'name',
			'phone',
			'email',
			'subject',
			'message',
		]

		# widgets = {

		# 'name' : forms.TextInput(
		#  	attrs={
  #       		'class': 'form-control',
  #       		'placeholder': 'Enter full name',
  #       	}),

  #       'phone' : forms.TextInput(
  #       	attrs={
  #       		'class': 'form-control',
  #       		'placeholder': 'Enter your phone number',
  #       	}),


  #   	'email' : forms.EmailInput(
		#  	attrs={
  #       		'class': 'form-control',
  #       		'placeholder': 'Ex: person@gmail.com',
  #       	}),

  #       'subject' : forms.TextInput(
  #       	attrs={
  #       		'class': 'form-control',
  #       	}),

		# 'message' : forms.TextInput(
		#  	attrs={
  #       		'class': 'vLargeTextField',
  #       		'cols': 50,
  #       	}),

  #      	}
    
