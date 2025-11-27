from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer

class SubmitReviewAPI(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order, OrderItem
from django.db.models import Sum, Count
from django.utils import timezone

class ManagerStatsAPI(APIView):
    def get(self, request, restaurant_id):
        print(f"\n📊 GRAPH REQUEST: Restaurant ID {restaurant_id}")
        
        try:
            # 1. Basic Filters
            orders = Order.objects.filter(restaurant_id=restaurant_id)
            print(f"Found {orders.count()} orders")

            # 2. Total Revenue (Handle None)
            total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum']
            if total_revenue is None:
                total_revenue = 0
            
            # 3. Today's Stats
            today = timezone.now().date()
            today_orders = orders.filter(created_at__date=today)
            today_revenue = today_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

            # 4. Top Selling Items
            # Note: values() returns a QuerySet, we convert to list
            top_items_qs = OrderItem.objects.filter(order__restaurant_id=restaurant_id)\
                .values('item__name')\
                .annotate(count=Count('id'))\
                .order_by('-count')[:5]
            
            top_items = list(top_items_qs)

            response_data = {
                "total_revenue": total_revenue,
                "total_orders": orders.count(),
                "today_revenue": today_revenue,
                "today_orders": today_orders.count(),
                "top_items": top_items
            }
            
            print("✅ Stats Data Ready:", response_data)
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ SERVER ERROR: {str(e)}")
            # Error ki detail frontend ko bhejo
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)