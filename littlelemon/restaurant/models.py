from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# 3 roles: Customer, Manager, Delivery Crew
class CustomUser(AbstractUser):
    # Define the choices (The "Sticker Colors")
    ROLE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('MANAGER', 'Manager'),
        ('DELIVERY', 'Delivery Crew'),
    )
    
    # Add the role field to the ID badge
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')

    def __str__(self):
        return f"{self.username} - {self.role}"



class Booking(models.Model):
    """
    Booking model representing table reservations
    """
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField()
    booking_date = models.DateTimeField()
    
    def __str__(self):
        return f"Booking for {self.name} on {self.booking_date}"

    class Meta:
        ordering = ['booking_date']



class Category(models.Model):

    name = models.CharField(max_length=100, db_index=True) # we put "db_index=True" because we will use this feature in search so it will be fast search
    description = models.TextField(blank=True)

    def __str__(self):

        return self.name



class MenuItems(models.Model):
    """
    Menu model representing menu items
    """

    # on_delete=models.CASCADE means if a Category is deleted, delete its items too.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    
    def __str__(self):
        return f"{self.title} - ${self.price}"

    class Meta:
        ordering = ['title']



class Cart(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)



class CartItem(models.Model):
    # This links specific menu items to the user's cart
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)



class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    

 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    # We save the exact price here. 
    # This acts like a photograph of the price. If you raise the menu price 
    # tomorrow, this past receipt won't magically change and upset your customer.
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)











