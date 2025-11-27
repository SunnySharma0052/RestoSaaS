from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import Category, Item
from tenants.models import Restaurant
from .serializers import CategorySerializer, ItemSerializer

class RestaurantMenuAPI(APIView):
    def get(self, request, restaurant_slug):
        try:
            # 1. Restaurant dhundo
            restaurant = Restaurant.objects.get(slug=restaurant_slug)
            
            # 2. Sirf us restaurant ki categories aur items nikalo
            categories = Category.objects.filter(restaurant=restaurant, is_active=True).prefetch_related('items', 'items__addons')
            
            # 3. JSON me convert karo
            serializer = CategorySerializer(categories, many=True, context={'request': request})
            
            return Response({
                "restaurant": restaurant.name,
                "menu": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        

# 1. Manager ke liye Saare Items ki list
class ManagerMenuItemsAPI(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        # Hum Category ke through filter karenge
        return Item.objects.filter(category__restaurant_id=restaurant_id)

# 2. Item Update API (Stock Out / Price Change)
class UpdateItemAPI(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer