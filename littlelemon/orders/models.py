from django.db import models
from django.conf import settings
from menu.models import MenuItems

 

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
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    # We save the exact price here. 
    # This acts like a photograph of the price. If you raise the menu price 
    # tomorrow, this past receipt won't magically change and upset your customer.
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)



