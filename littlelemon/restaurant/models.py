from django.db import models


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


class Menu(models.Model):
    """
    Menu model representing menu items
    """
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    
    def __str__(self):
        return f"{self.title} - ${self.price}"

    class Meta:
        ordering = ['title']







