from rest_framework.permissions import BasePermission, SAFE_METHODS


"""

2. How to use it in your Views (views.py)
Now, instead of importing different classes, you import the one master class and simply declare who is allowed at the top of your view.

Python
from rest_framework import viewsets
from .permissions import HasRequiredRole
from .models import Order

class DeliveryDashboardViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    # Plug in the master bouncer
    permission_classes = [HasRequiredRole]
    
    # Hang the sign above the door: Who is allowed here?
    required_roles = ['MANAGER', 'DELIVERY']

"""

class HasRequiredRole(BasePermission):
    """
    Checks if the user's role matches the 'required_roles' list 
    defined inside the View.
    """
    def has_permission(self, request, view):

        # 0. Let anyone browse (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # 1. Reject unauthenticated users immediately
        if not request.user or not request.user.is_authenticated:
            return False
            
        # 2. Look for the 'required_roles' sign on the view
        # If the view doesn't have the sign, deny access by default for safety
        required_roles = getattr(view, 'required_roles', [])
        
        # 3. Check if the user's role is in the allowed list
        return request.user.role in required_roles




class IsManagerOnly(BasePermission):
    """
    Strict permission that only allows access to users with the 'manager' role.
    ALL HTTP methods (GET, POST, PUT, PATCH, DELETE, etc.) are blocked for non-managers.
    Returns 401/403 for everyone except managers.
    """
    def has_permission(self, request, view):
        # 1. Reject unauthenticated users immediately
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Only allow users whose role is exactly 'manager'
        return getattr(request.user, 'role', None) == 'MANAGER'

