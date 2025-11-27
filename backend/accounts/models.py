from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Roles define karte hain
    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin'),      # App Owner (Aap)
        ('RESTAURANT_ADMIN', 'Restaurant Owner'), # Restaurant ka Malik
        ('MANAGER', 'Manager'),
        ('WAITER', 'Waiter'),
        ('KITCHEN', 'Kitchen Staff'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='RESTAURANT_ADMIN')
    
    # Ye user kis restaurant ka staff hai? (Link to Tenant)
    # Note: 'tenants.Restaurant' string mein likha hai kyunki abhi wo model bana nahi hai
    restaurant = models.ForeignKey('tenants.Restaurant', on_delete=models.CASCADE, null=True, blank=True, related_name='staff')

    def __str__(self):
        return f"{self.username} - {self.role}"