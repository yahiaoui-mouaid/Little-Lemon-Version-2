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

