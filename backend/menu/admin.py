from django.contrib import admin
from .models import Category, Item, ItemAddon

class ItemAddonInline(admin.TabularInline):
    model = ItemAddon
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'is_active')
    list_filter = ('restaurant',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_veg', 'is_available')
    list_filter = ('category__restaurant', 'is_available', 'is_veg')
    search_fields = ('name',)
    
    # Item create karte waqt hi Add-ons add karne ka option
    inlines = [ItemAddonInline]