from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection


# Create your views here.
def home(request):
	return render(request, 'users/dashboard.html')
	
def loginPage(request):
	if request.user.is_authenticated:
		return redirect('profile')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			
			user = authenticate(request, username=username, password=password)
			
			if user is not None:
				login(request, user)
				return redirect('profile')
			else:
				messages.info(request, 'Username or password is incorrect')
		return render(request,'users/login.html')

def logoutUser(request):
	logout(request)
	return redirect('logoutPage')
	
def logoutPage(request):
	return render(request, 'users/logout.html')
	
def contact(request):
	return render(request, 'users/contact.html')

@login_required(login_url='login')
def rides(request):
	query = 'SELECT * FROM users_ride r ORDER BY r.datetime DESC'
	c = connection.cursor()
	c.execute(query)
	rides = c.fetchall()
	return render(request, 'users/rides.html',{'rides':rides})

def searchrides(request):
	search1 = request.GET.get('pickup')
	search2 = request.GET.get('dropoff')
	query = 'SELECT * FROM users_ride r WHERE r.origin ~\'%s\' AND r.destination ~ \'%s\''%(search1,search2)
	c = connection.cursor()
	c.execute(query)
	rides = c.fetchall()
	return render(request, 'users/searchrides.html',{'rides':rides})

def register(request):
	template = 'users/register.html'
	if request.user.is_authenticated:
		return redirect('profile')
	else:
		if request.method == 'POST':
			# create a form instance and populate it with data from the request:
			form = RegisterForm(request.POST)
			# check whether it's valid:
			if form.is_valid():
				if Users.objects.filter(username=form.cleaned_data['username']).exists():
					return render(request, template, {
						'form': form,
						'error_message': 'Username already exists.'
					})
				elif Users.objects.filter(email=form.cleaned_data['email']).exists():
					return render(request, template, {
						'form': form,
						'error_message': 'Email already exists.'
					})
				elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
					return render(request, template, {
						'form': form,
						'error_message': 'Passwords do not match.'
					})
				else:
					user = Users.objects.create_user(
						form.cleaned_data['username'],
						form.cleaned_data['password1'],
					)
					user.email = form.cleaned_data['email']
					user.name = form.cleaned_data['name']
					user.number = form.cleaned_data['number']
					user.save()
				   
					# Login the user
					login(request, user)
				   
					# redirect to accounts page:
					return redirect('profile')
   # No post data availabe, let's just show the page.
		else:
			form = RegisterForm()

		return render(request, template, {'form': form})

@login_required(login_url='login')
def profile(request):
	if request.user.is_authenticated:
		userid = request.user.id
		license = """ SELECT v.license
					  FROM users_users u, users_vehicle v
					  WHERE u.id = v.username_id
					  AND u.id = '%s' """%(userid)
		f = connection.cursor()
		f.execute(license)
		profilelicense = f.fetchone()
		
		username = request.user.username
		profilebids = """SELECT r.origin, r.destination, r.datetime, b.status 
					   FROM users_users u, users_bid b, users_ride r
					   WHERE b.username_id = u.id
					   AND r.rideid = b.rideid_id
					   AND u.username ='%s'
					   ORDER BY r.datetime DESC"""%(username)
		c = connection.cursor()
		c.execute(profilebids)
		bids = c.fetchall()
		
		profileride = """ SELECT u.username, r.origin, r.destination, r.datetime, b.bidtime
						  FROM users_users u, users_bid b, users_ride r, users_vehicle v
						  WHERE u.id = b.username_id
						  AND r.rideid = b.rideid_id
						  AND v.license = r.license_id
						  AND v.username_id = '%s'
						  ORDER BY b.bidtime, b.status"""%(userid)
		d = connection.cursor()
		d.execute(profileride)
		passengers = d.fetchall()
		
		ownrides = """ SELECT r.origin, r.destination, r.datetime, r.seats, r.price, r.rideid
						   FROM users_ride r, users_vehicle v
						   WHERE r.license_id = v.license
						   AND v.username_id = '%s'
						   ORDER BY r.datetime DESC """ %(userid)
		e = connection.cursor()
		e.execute(ownrides)
		ridelist = e.fetchall()
		context = { 'profilelicense':profilelicense, 'bids':bids , 'passengers':passengers, 'ridelist':ridelist}
	return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def addride(request):
	if request.method == 'POST':
		form = RideForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('profile')
	else:
		form = RideForm()
	return render(request, 'users/addride.html', {'form':form})

@login_required(login_url='login')
def addcar(request):
	if request.method == 'POST':
		form = CarForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('profile')
	else:
		form = CarForm()
	return render(request, 'users/addcar.html', {'form':form})
	
@login_required(login_url='login')
def bidride(request):
	if request.method == 'POST':
		form = BidForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('profile')
	else:
		form = BidForm()
	return render(request, 'users/bids.html', {'form':form})
	
@login_required(login_url='login')
def deleteride(request):
	ride = request.GET.get('rideid')
	if Ride.objects.filter(rideid=ride).exists():
		deletion= """DELETE FROM users_bid b WHERE b.rideid_id ='%s'"""%(ride)
		delete ="""DELETE FROM users_ride r WHERE r.rideid ='%s'"""%(ride)
		c = connection.cursor()
		c.execute(deletion)
		d = connection.cursor()
		d.execute(delete)
		return redirect('profile')

	return render(request, 'users/deleteride.html')
	