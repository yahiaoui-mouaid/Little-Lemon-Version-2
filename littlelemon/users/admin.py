from django.contrib import admin
from django.contrib import admin
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


