import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order

class CreatePaymentAPI(APIView):
    def post(self, request, *args, **kwargs):
        order_db_id = request.data.get('order_id') # Hamare database ka order ID
        
        try:
            order = Order.objects.get(id=order_db_id)
            
            # 1. Razorpay Client initialize karein
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # 2. Razorpay Order Create karein (Amount paise me hota hai, so * 100)
            payment_data = {
                "amount": int(order.total_amount * 100), 
                "currency": "INR",
                "receipt": f"order_rcptid_{order.id}"
            }
            
            razorpay_order = client.order.create(data=payment_data)
            
            return Response({
                "id": razorpay_order['id'], # Razorpay ka Order ID
                "amount": razorpay_order['amount'],
                "key_id": settings.RAZORPAY_KEY_ID,
                "order_id": order.id # Hamara DB ID
            })
            
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)