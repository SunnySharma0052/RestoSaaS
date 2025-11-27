from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price_at_time_of_order',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'restaurant', 'table', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('restaurant', 'status', 'payment_status', 'created_at')
    inlines = [OrderItemInline]
    
    # Admin se status change karne ke liye
    list_editable = ('status', 'payment_status')