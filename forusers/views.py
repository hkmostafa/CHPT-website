from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.db.models import Q
# Create your views here.
from .forms import RdvForm , SpecialtyForm, DoctorForm, RegisterForm, AdminRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Appointment,Doctor,Specialty
from contactus.models import Contact




#---------------------------------------USERS VIEWS-------------------------------------------

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created !, You can login now')
			return redirect('login')
	else:
		form = RegisterForm()
	return render(request, 'forusers/register.html', {'form': form})    


def userlogin(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			if user.groups.filter(name='admin'):
				login(request, user)
				return redirect('profile')
			elif user.groups.filter(name='doctor'):
				login(request, user)
				return redirect('profile')
			else:
				login(request, user)
				return redirect('profile')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'forusers/login.html', context)


@login_required
def UpdateUser(request, id):
	user = User.objects.get(id=id)
	userform=UserUpdateForm(instance=user)
	if request.method == 'POST':
		userform = UserUpdateForm(request.POST, instance=user)
		if userform.is_valid(): 	
			userform.save()
			messages.success(request, f'User has been updated')	
			return redirect('adminuser')
	context = {
		'userform': userform,
		'user' : user,
	}
	return render(request, 'forusers/user_modify.html', context) 

@login_required
def AdminCreateAdmin(request):
	if request.method == 'POST':
		form = AdminRegisterForm(request.POST)
		if form.is_valid():
			user=form.save()
			# group = Group.objects.get(name='doctor')
			# user = form.cleaned_data.get('username')
			# user.groups.add(group)
			
			group = Group.objects.get(name='admin')
			user.groups.add(group)
			messages.success(request, f'Admin account has been created !')
			return redirect('adminuser')
	else:
		form = AdminRegisterForm()
	return render(request, 'forusers/user_add_admin.html', {'form': form}) 



@login_required
def AdminCreateDoctor(request):
	if request.method == 'POST':
		user_form = AdminRegisterForm(request.POST)
		doctor_form = DoctorForm(request.POST)
		if user_form.is_valid() and doctor_form.is_valid():
			# group = Group.objects.get(name='doctor')
			# user = form.cleaned_data.get('username')
			# user.groups.add(group)
			user=user_form.save()
			doctor_form.save()
			group = Group.objects.get(name='doctor')
			user.groups.add(group)
			messages.success(request, f'Doctor account has been created !')
			return redirect('adminuser')
	else:
		user_form = AdminRegisterForm()
		doctor_form = DoctorForm()
	context={
		'user_form': user_form,
		'doctor_form': doctor_form,
		}
	return render(request, 'forusers/user_add_doctor.html', context)       


@login_required
def AdminDeleteUser(request, id):
	user = User.objects.get(id=id)
	if request.method == "POST":
		if user.groups.filter(name='doctor'):
			doctor=Doctor.objects.get(doctor_name=user.username)
			doctor.delete()
		user.delete()
		messages.success(request, f'User has been deleted')
		return redirect('adminuser')

	context = {'user':user}
	return render(request, 'forusers/user_delete.html', context)


@login_required
def profile(request):
	user=request.user

	#-----------------------DOCTOR---------------------

	if user.groups.filter(name='doctor'):
		appointment_list=filter_doc_appointments(request)
		if request.method == 'POST':
			u_form = UserUpdateForm(request.POST, instance=request.user)
			p_form = ProfileUpdateForm(request.POST,
									   request.FILES,
									   instance=request.user.profile)
			if u_form.is_valid() and p_form.is_valid():
				u_form.save()
				p_form.save()
				messages.success(request, f'Your account has been updated!')
				return redirect('profile')

		else:
			u_form = UserUpdateForm(instance=request.user)
			p_form = ProfileUpdateForm(instance=request.user.profile)
		context={
		'u_form': u_form,
		'p_form': p_form,
		'appointments': appointment_list
		}
		return render(request, 'forusers/doctorprofile.html',context)


	#-----------------------ADMIN---------------------

	elif user.groups.filter(name='admin'):
		context={
		}
		return render(request, 'forusers/adminprofile.html')

	#-----------------------USER---------------------

	else:
		if request.method == 'POST':
			u_form = UserUpdateForm(request.POST, instance=request.user)
			p_form = ProfileUpdateForm(request.POST,
									   request.FILES,
									   instance=request.user.profile)
			if u_form.is_valid() and p_form.is_valid():
				u_form.save()
				p_form.save()
				messages.success(request, f'Your account has been updated!')
				return redirect('profile')

		else:
			u_form = UserUpdateForm(instance=request.user)
			p_form = ProfileUpdateForm(instance=request.user.profile)

		context = {
			'u_form': u_form,
			'p_form': p_form,
			'appointments': Appointment.objects.filter(user=request.user).order_by('app_date'),
		}

		return render(request, 'forusers/profile.html', context)

#----------------------- SOMETHING ---------------------

def is_valid_queryparam(param):
	return param != '' and param is not None


#----------------------- ADMIN APPOINTMENTS LIST ---------------------

@login_required
def admin_app(request):
	appointment_list = filter_appointments(request)
	page = request.GET.get('page', 1)

	paginator = Paginator(appointment_list, 8)
	
	try:
		appointments = paginator.page(page)
	except PageNotAnInteger:
		appointments = paginator.page(1)
	except EmptyPage:
		appointments = paginator.page(paginator.num_pages)
	context={
		'appointments' : appointments,
	}
	return render(request, 'forusers/admin_appointments.html',context)

	#----------------------- APPOINTMENT QUERY ---------------------
@login_required
def filter_appointments(request):
	qs = Appointment.objects.all()

	user_patient_service_search=request.GET.get('user_patient_service')

	if is_valid_queryparam(user_patient_service_search):
		qs = qs.filter(Q(user__username__icontains=user_patient_service_search) 
		| Q(patient_name__icontains=user_patient_service_search) 	
		| Q(specialty__specialty_name__icontains=user_patient_service_search)).distinct()
		
	return qs

@login_required
def filter_doc_appointments(request):
	user=request.user
	date=Appointment.objects.all().filter(doctor__doctor_name=user.username)
	date_search=request.GET.get('date_search')

	if is_valid_queryparam(date_search):
		date=date.filter(app_date__iexact=date_search)
	return date
#----------------------- ADMIN USERS LIST ---------------------

@login_required
def admin_user(request):
	user_list = filter_users(request)
	page = request.GET.get('page', 1)

	paginator = Paginator(user_list, 8)
	
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	context={
		'users': users,
	}
	return render(request, 'forusers/admin_users.html',context)


	#----------------------- USER QUERY ---------------------

@login_required
def filter_users(request):
	user = User.objects.all().order_by('groups')
	username_search=request.GET.get('username')

	if is_valid_queryparam(username_search):
		 user = user.filter(username__icontains=username_search)
		
	return user	

#----------------------- ADMIN CONTACTS LIST ---------------------

@login_required
def admin_cont(request):
	contact_list=filter_contacts(request)
	page = request.GET.get('page', 1)

	paginator = Paginator(contact_list, 8)
	
	try:
		contacts= paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)
	context={
		'contacts': contacts
	}
	return render(request, 'forusers/admin_contacts.html',context)

	#----------------------- CONTACTS QUERY ---------------------
@login_required
def filter_contacts(request):
	contact = Contact.objects.all()
	sender_subject_search=request.GET.get('sender_subject')

	if is_valid_queryparam(sender_subject_search):
		contact = contact.filter(Q(name__icontains=sender_subject_search) 
		| Q(subject__icontains=sender_subject_search)).distinct()
		
	return contact	

#----------------------- ADMIN SPECIALTIES LIST ---------------------
login_required
def admin_spec(request):
	specialty_list=filter_specialties(request)
	page = request.GET.get('page', 1)

	paginator = Paginator(specialty_list, 10)
	
	try:
		specialties= paginator.page(page)
	except PageNotAnInteger:
		specialties = paginator.page(1)
	except EmptyPage:
		specialties = paginator.page(paginator.num_pages)
	context={
		'specialties': specialties
	}
	return render(request, 'forusers/admin_specialties.html',context)
	#----------------------- SPECIALTY QUERY ---------------------
@login_required
def filter_specialties(request):
	specialty = Specialty.objects.all()
	specialty_search=request.GET.get('specialty_search')

	if is_valid_queryparam(specialty_search):
		specialty = specialty.filter(specialty_name__icontains=specialty_search) 
		
	return specialty	




@login_required(login_url='login')
def CreateRdv(request):
	
	if request.method == 'POST':
		rdvform = RdvForm(request.POST)
		if rdvform.is_valid():
			instance = rdvform.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, f'You have booked an appointment ! You modify or delete it here')
			return redirect('profile')  
	else:   
		rdvform = RdvForm()         
		
	return render(request, 'forusers/appointment.html', {'rdvform': rdvform})


@login_required
def UpdateRdv(request, id):
	user=request.user
	appointment = Appointment.objects.get(id=id)
	rdvform=RdvForm(instance=appointment)
	if request.method == 'POST':
		rdvform = RdvForm(request.POST, instance=appointment)
		if rdvform.is_valid(): 	
			rdvform.save()
			messages.success(request, f'Your appointment has been updated')
			return redirect('profile')
	context = {
		'rdvform': rdvform,
		'appointment' : appointment,
	}
	return render(request, 'forusers/appointment_modify.html', context) 


@login_required
def DeleteRdv(request, id):
	appointment = Appointment.objects.get(id=id)
	if request.method == "POST":
		appointment.delete()
		messages.success(request, f'Your appointment has been deleted')
		return redirect('profile')

	context = {'appointment':appointment}
	return render(request, 'forusers/appointment_delete.html', context)


def load_doctors(request):
	specialty_id = request.GET.get('specialty')
	doctors = Doctor.objects.filter(specialty_id=specialty_id).order_by('doctor_name')
	return render(request, 'forusers/doctors_dropdown_list_options.html', {'doctors': doctors})




#---------------------------------------CONTACTS VIEWS-------------------------------------------
@login_required
def DeleteContact(request, id):
	contact = Contact.objects.get(id=id)
	if request.method == "POST":
		contact.delete()
		messages.success(request, f'Contact has been deleted')
		return redirect('admincont')

	context = {'contact':contact}
	return render(request, 'forusers/contact_delete.html', context)



#---------------------------------------SPECIALTIES VIEWS-------------------------------------------
@login_required
def AdminCreateSpecialty(request):
	if request.method == 'POST':
		form=SpecialtyForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,f'Specialty has been created successfully')
			return redirect('adminspec')
	else:
		form=SpecialtyForm()
	context={'form':form}
	return render(request, 'forusers/specialty_add.html',context)

@login_required
def AdminUpdateSpecialty(request, id):
	specialty = Specialty.objects.get(id=id)
	form=SpecialtyForm(instance=specialty)
	if request.method == 'POST':
		form = SpecialtyForm(request.POST, instance=specialty)
		if form.is_valid(): 	
			form.save()
			messages.success(request, f'Specialty has been updated')
			return redirect('adminspec')
	context = {
		'form': form,
		'specialty' : specialty,
	}
	return render(request, 'forusers/specialty_modify.html', context) 

@login_required
def AdminDeleteSpecialty(request, id):
	specialty = Specialty.objects.get(id=id)
	if request.method == "POST":
		specialty.delete()
		messages.success(request, f'Specialty has been deleted')
		return redirect('adminspec')

	context = {'specialty':specialty}
	return render(request, 'forusers/specialty_delete.html', context)










	