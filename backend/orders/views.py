from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer, OrderDetailSerializer

class CreateOrderAPI(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer




# ... Purana CreateOrderAPI waisa hi rahne dein ...

# 1. Sare Orders dekhne ke liye (Kitchen View)
class StaffOrderListAPI(generics.ListAPIView):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        # URL se restaurant_id lenge
        restaurant_id = self.kwargs['restaurant_id']
        # Sirf wo orders dikhao jo complete nahi huye (Pending, Preparing, Ready)
        return Order.objects.filter(restaurant_id=restaurant_id).exclude(status='COMPLETED').order_by('-created_at')

# 2. Order ka Status badalne ke liye (Pending -> Preparing)
class UpdateOrderStatusAPI(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        # Ye 'partial=True' ensure karega ki hum sirf status update kar sakein
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)