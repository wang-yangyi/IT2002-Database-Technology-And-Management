from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, username, password):
		if not username:
			raise ValueError('Username required!')
		user = self.model( username=username, password=password)
		user.set_password(password)
		user.save(using=self._db)
		return user
		
	def create_superuser(self, username, password):
		user = self.create_user( username=username, password=password )
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user
	
class Users(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=30,unique=True)
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=60,unique=True)
	number = models.CharField(max_length=12,unique=True)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login',auto_now=True,null=True)
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []
	
	objects = UserManager()
	
	def __str__(self):
		return self.username

class Vehicle(models.Model):
	username = models.ForeignKey(Users, on_delete= models.CASCADE)
	license = models.CharField(max_length=32, primary_key=True)
	model = models.CharField(max_length=32)
	carplate = models.CharField(max_length=32)
	def __str__(self):
		return self.license
	
class Ride(models.Model):
	license = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
	rideid = models.AutoField(primary_key=True)
	origin = models.CharField(max_length=50)
	destination = models.CharField(max_length=50)
	datetime = models.DateTimeField()
	seats = models.IntegerField()
	price = models.FloatField()	
	
	def __str__(self):
		return str(self.rideid)
		
class Bid(models.Model):
	STATUS = (
		('Pending','Pending'),
		('Rejected','Rejected'),
		('Accepted','Accepted'),
		)
	username = models.ForeignKey(Users, on_delete=models.CASCADE)
	rideid = models.ForeignKey(Ride, on_delete=models.CASCADE)
	bidtime= models.DateTimeField(auto_now_add=True)
	status= models.CharField(max_length=50, choices=STATUS, default='Pending')
	
	
