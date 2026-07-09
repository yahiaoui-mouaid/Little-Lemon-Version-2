from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from menu.models import MenuItems
from menu.serializers import MenuSerializer




class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    # 1. Tell the serializer to look inside the 'item' relation and grab the 'name'
    item_name = serializers.ReadOnlyField(source='item.title')
    item_price = serializers.ReadOnlyField(source='item.price')
    class Meta:
        model = CartItem
        fields = ['id', 'item','item_name', 'item_price', 'quantity']
 


class OrderItemSerializer(serializers.ModelSerializer):
    """
    A single line item inside an order.
 
    Read: nests the menu item's details for a self-contained response.
    Write: accepts `item_id` + `quantity`; `price_at_time` stays read-only
    since it should be captured server-side at order-creation time,
    never trusted from the client.
    """
 
    item = MenuSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItems.objects.all(), source="item", write_only=True
    )
    subtotal = serializers.SerializerMethodField()
 
    class Meta:
        model = OrderItem
        fields = ["id", "item", "item_id", "quantity", "price_at_time", "subtotal"]
        read_only_fields = ["price_at_time"]
 
    def get_subtotal(self, obj):
        return obj.quantity * obj.price_at_time
 
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value
 
 
class OrderSerializer(serializers.ModelSerializer):
    """
    Standard order representation — used for a customer's own order history.
    `user` is shown as a readable username, not writable (the view sets it
    from request.user).
    """
 
    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()
 
    class Meta:
        model = Order
        fields = ["id", "user", "items", "items_count", "total_price", "date_ordered"]
        read_only_fields = ["total_price", "date_ordered"]
 
    def get_items_count(self, obj):
        return obj.items.count()


