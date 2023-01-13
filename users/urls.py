from django.urls import path
from .import views
from users.views import (
	register,
)

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('loggedout/',views.logoutPage, name = 'logoutPage'),
    path('register/',views.register, name='register'),
    path('contact/',views.contact, name='contact'),
    path('rides/',views.rides, name='rides'),
    path('profile/',views.profile, name='profile'),
    path('searchrides/',views.searchrides, name='searchrides'),
    path('addride/', views.addride, name="addride"),
    path('addcar/',views.addcar, name="addcar"),
    path('bids/',views.bidride, name="bid"),
    path('delete/', views.deleteride, name ='deleteride'),
]