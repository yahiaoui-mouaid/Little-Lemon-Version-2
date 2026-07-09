from django.contrib import admin
from .models import MenuItems, Category


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

