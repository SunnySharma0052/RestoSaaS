from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    # List me ye columns dikhenge
    list_display = ['username', 'email', 'role', 'restaurant', 'is_staff']
    
    # Edit page par Role aur Restaurant select karne ka option aayega
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'restaurant')}),
    )

admin.site.register(User, CustomUserAdmin)