from rest_framework import serializers
from .models import Booking, MenuItems, Category, Cart, CartItem, Order, OrderItem
from django.contrib.auth import get_user_model 


""" New Information in security:
Attack Surface Reduction (The "Principle of Least Privilege"):
The Risk: Using fields = '__all__' exposes everything. 
If you add a hidden internal field later (like is_hidden_from_public), it will automatically be exposed to the API.
The Fix: Never use __all__ for sensitive or write-heavy endpoints. 
Explicitly list what fields the user is allowed to send.
"""

User = get_user_model()

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']
        read_only_fields = ['id', 'username']

    # make only the "manager" able to cha,ge users roles
    def validate_role(self, value):
            # 1. Get the current user making the request
            request = self.context.get('request')
            if not request or not request.user:
                raise serializers.ValidationError("Authentication required.")

            # 2. Skip check if it's a new user registration (instance doesn't exist yet)
            if not self.instance:
                return value

            # 3. If the role is actually changing, block it unless they are a MANAGER
            if self.instance.role != value and request.user.role != 'MANAGER':
                raise serializers.ValidationError("Only managers can change user roles.")

            return value



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        # fields = '__all__'  # Exposes id, name, no_of_guests, and booking_date
        fields = ['id', 'name', 'no_of_guests', 'booking_date']



class MenuSerializer(serializers.ModelSerializer):

        # Concierge: Show the actual category name, not just a number (ID)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItems
        # fields = '__all__'  # Exposes id, title, price, and inventory (Not secure) 
        fields = ['id', 'category', 'category_name', 'title', 'price', 'inventory']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters.")
        return value.strip()



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    # 1. Tell the serializer to look inside the 'item' relation and grab the 'name'
    item_name = serializers.ReadOnlyField(source='item.title')
    class Meta:
        model = CartItem
        fields = ['id', 'item','item_name', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'



class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name'] # Strictly limit the output to the name


