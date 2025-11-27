from django.db import models
from tenants.models import Restaurant

class Category(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)  # e.g., Starters, Drinks
    description = models.TextField(blank=True)
    sort_order = models.IntegerField(default=0) # Menu me upar/niche dikhane ke liye
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"

    class Meta:
        verbose_name_plural = "Categories"


class Item(models.Model):
    SPICE_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    
    # Status
    is_available = models.BooleanField(default=True) # Stock Out feature ke liye
    
    # Dietary Tags (Requirement 1.A)
    is_veg = models.BooleanField(default=True)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    spice_level = models.CharField(max_length=10, choices=SPICE_CHOICES, default='MEDIUM')

    def __str__(self):
        return self.name


class ItemAddon(models.Model):
    # Requirement 1.B: Customizations & add-ons (extra cheese, etc.)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='addons')
    name = models.CharField(max_length=100) # e.g., Extra Cheese
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.item.name} - {self.name} (+{self.price})"