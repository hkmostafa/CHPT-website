from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import ContactForm
from django.contrib import messages

# Create your views here.

def ContactView(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			form =ContactForm()
			messages.success(request, f'Thanks for your submission!')
		return redirect('home')

	else:	
		form = ContactForm()

	return render(request, 'contactus/contact.html', {'form': form}) 	