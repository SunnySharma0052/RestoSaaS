from rest_framework import serializers
from .models import Order, OrderItem
from menu.models import Item

class OrderItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField() # Frontend hume Item ID bheje

    class Meta:
        model = OrderItem
        fields = ['item_id', 'quantity', 'notes', 'customizations']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'restaurant', 'table', 'total_amount', 'status', 'items']
        read_only_fields = ['order_id', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # 1. Naya Order banao
        import uuid
        order = Order.objects.create(
            order_id=f"ORD-{str(uuid.uuid4())[:8].upper()}", # Unique ID auto-generate
            **validated_data
        )

        total_bill = 0

        # 2. Items ko Order ke sath jodo
        for item_data in items_data:
            item_id = item_data.pop('item_id')
            item_obj = Item.objects.get(id=item_id)
            
            # Price calculate karo
            item_total = item_obj.price * item_data.get('quantity', 1)
            total_bill += item_total
            
            OrderItem.objects.create(
                order=order, 
                item=item_obj, 
                price_at_time_of_order=item_obj.price,
                **item_data
            )

        # 3. Total amount update karo
        order.total_amount = total_bill
        order.save()
        
        return order
    

    # Is file ke neeche ye add karein:

# Staff ke liye detailed serializer
class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    table_number = serializers.CharField(source='table.table_number', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'table_number', 'status', 'payment_status', 'total_amount', 'created_at', 'items']