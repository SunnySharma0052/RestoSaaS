from rest_framework import serializers
from .models import Category, Item, ItemAddon

class ItemAddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAddon
        fields = ['id', 'name', 'price']

class ItemSerializer(serializers.ModelSerializer):
    addons = ItemAddonSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'image', 'is_veg', 'is_vegan', 'spice_level', 'addons', 'is_available']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'items']