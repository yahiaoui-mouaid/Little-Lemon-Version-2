from rest_framework import serializers
from .models import Booking


""" New Information in security:
Attack Surface Reduction (The "Principle of Least Privilege"):
The Risk: Using fields = '__all__' exposes everything. 
If you add a hidden internal field later (like is_hidden_from_public), it will automatically be exposed to the API.
The Fix: Never use __all__ for sensitive or write-heavy endpoints. 
Explicitly list what fields the user is allowed to send.
"""


 

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        # fields = '__all__'  # Exposes id, name, no_of_guests, and booking_date
        fields = ['id', 'name', 'no_of_guests', 'booking_date']



