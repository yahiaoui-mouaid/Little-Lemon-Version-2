from django.contrib import admin
from .models import Booking, Menu

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


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """
    Admin configuration for Menu model
    """
    list_display = ['id', 'title', 'price', 'inventory']
    list_filter = ['inventory']
    search_fields = ['title']
    ordering = ['title']
    readonly_fields = ['id']




