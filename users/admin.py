from django.contrib import admin

# Register your models here.

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin, AdminPasswordChangeForm

# Register your models here.
from .models import *
from .forms import UserChangeForm, UserCreationForm

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Personal info', {'fields': ('name', 'number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'name', 'is_superuser')
    list_filter = ( 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)
    readonly_fields = ('last_login', 'date_joined',)

	
admin.site.register(Users, CustomUserAdmin)
class VehicleAdmin(admin.ModelAdmin):
	list_display = ['username','license','carplate','model']
	
admin.site.register(Vehicle, VehicleAdmin)

class RideAdmin(admin.ModelAdmin):
	list_display = ['license','rideid','origin','destination','datetime']

class BidAdmin(admin.ModelAdmin):
	def get_rideid(self, obj):
		return obj.rideid.name
	get_rideid.short_description = 'Ride ID'
	get_rideid.admin_order_field = 'rideid'
	list_display = ['username','rideid','bidtime','status']

admin.site.register(Bid, BidAdmin)
admin.site.register(Ride, RideAdmin)