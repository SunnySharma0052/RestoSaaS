from django.db import models
from tenants.models import Restaurant, Table
from menu.models import Item

class Order(models.Model):
    # Requirement 1.B: Live order status
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),        # Customer ne bheja, Staff ne nahi dekha
        ('ACCEPTED', 'Accepted'),      # Staff ne accept kiya
        ('PREPARING', 'Preparing'),    # Kitchen me ban raha hai
        ('READY', 'Ready to Serve'),   # Ban gaya
        ('SERVED', 'Served'),          # Table par pahunch gaya
        ('COMPLETED', 'Completed'),    # Payment done & customer left
        ('CANCELLED', 'Cancelled'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, related_name='orders')
    
    # Tracking
    order_id = models.CharField(max_length=20, unique=True) # E.g., ORD-1001
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.table}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    # Requirement: Customizations & Add-ons store karne ke liye (JSON format)
    # Example data: {"Extra Cheese": 50, "Spicy": 0}
    customizations = models.JSONField(default=dict, blank=True)
    
    # Requirement: Order notes (e.g., "No onions")
    notes = models.CharField(max_length=255, blank=True, null=True)
    
    price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2) # Agar menu price badle to purane order par asar na pade

    def __str__(self):
        return f"{self.quantity}x {self.item.name}"

    def save(self, *args, **kwargs):
        # Auto-save price if not set
        if not self.price_at_time_of_order:
            self.price_at_time_of_order = self.item.price
        super().save(*args, **kwargs)