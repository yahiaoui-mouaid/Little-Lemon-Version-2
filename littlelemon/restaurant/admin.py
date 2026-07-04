from django.contrib import admin
from .models import Booking, MenuItems, Category, Cart, CartItem, Order, OrderItem
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # This adds the role field when you are EDITING a user
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Role Assignment', {'fields': ('role',)}),
    )
    
    # This adds the role field when you are CREATING a user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Role Assignment', {'fields': ('role',)}),
    )

# Register your custom user model with the custom admin layout
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for Booking model
    """
    list_display = ['id', 'name', 'no_of_guests', 'booking_date']
    list_filter = ['booking_date', 'no_of_guests']
    search_fields = ['name']
    ordering = ['-booking_date']
    date_hierarchy = 'booking_date'
    readonly_fields = ['id']


@admin.register(MenuItems)
class MenuAdmin(admin.ModelAdmin):
    """
    Admin configuration for Menu model
    """
    list_display = ['id', 'title', 'price', 'inventory', 'category']
    list_filter = ['category']
    search_fields = ['title']
    ordering = ['title']
    readonly_fields = ['id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']  # Fast search due to db_index=True on name field
    list_filter = ['name']
    ordering = ['name']



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






