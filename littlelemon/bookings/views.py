from .serializers import BookingSerializer 
from .models import Booking
from rest_framework import viewsets
from users.permissions import HasRequiredRole



# He can See the menu items (all can do it) + create/delete/patch/put menu items (if he is the manager or the )


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    permission_classes = [HasRequiredRole]
    
    # as long as he is logged in he can Book
    required_roles = ['MANAGER', 'DELIVERY', 'CUSTOMER']
    
