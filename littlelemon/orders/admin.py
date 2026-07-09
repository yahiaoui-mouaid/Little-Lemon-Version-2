from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # What columns to show
    list_display = ['id', 'user']
    # Adds a search bar to find carts by username
    search_fields = ['user__username']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'item', 'quantity']
    # Adds a sidebar to filter items by which cart they belong to
    list_filter = ['cart']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'date_ordered']
    list_filter = ['date_ordered']
    search_fields = ['user__username']
    

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'item', 'quantity', 'price_at_time']
    list_filter = ['order']


