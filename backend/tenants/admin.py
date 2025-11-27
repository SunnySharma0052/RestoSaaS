from django.contrib import admin
from .models import Restaurant, Table

# Admin panel me Restaurant dikhane ke liye
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'phone_number', 'is_active')

# Admin panel me Table dikhane ke liye
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'table_number', 'qr_code_link')