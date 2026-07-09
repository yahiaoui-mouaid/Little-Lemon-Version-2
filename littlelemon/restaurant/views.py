from django.shortcuts import render
from .serializers import (BookingSerializer, MenuSerializer, CartItemSerializer,
                           OrderSerializer, UserRoleSerializer, CategorySerializer, CategoryNameSerializer)

from .models import Booking, MenuItems, Cart, CartItem, Order, OrderItem, CustomUser, Category
from rest_framework import viewsets
from .permissions import HasRequiredRole, IsManagerOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from .filters import OrderFilter







def home_page(request):
    return render(request, 'home.html', {})


def signup_page(request):
    # This grabs the HTML file and sends it to the user's screen
    return render(request, 'signup.html')

def login_page(request): 
    return render(request, 'login.html')

def logout_page(request):
    return render(request, 'logout.html')

def about_page(request):
    return render(request, 'about.html')

def book_table_page(request):
    return render(request, 'book_table.html')

def menu_page(request):
    return render(request, 'menu.html')

def menu_item_page(request, pk):
    return render(request, 'menu_item.html')


def menu_item_create(request):
    return render(request, 'create_menu_item.html')


def create_category(request):
    return render(request, 'create_category.html')


def members_page(request):
    return render(request, 'members.html')


def order_confirmation_page(request):
    return render(request, 'order_confirmation.html')

def myorders_page(request):
    return render(request, 'myorders.html')

def dashboard_page(request):
    return render(request, 'dashboard.html')








 # because of DefaultRouter i don't need to create another view for single item view " he creates it for me :) "




class MembersDataAPI(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsManagerOnly]
    


# He can See the menu items (all can do it) + create/delete/patch/put menu items (if he is the manager or the )

class MenuView(viewsets.ModelViewSet): # because of DefaultRouter i don't need to create another view for single item view " he creates it for me :) "
    queryset = MenuItems.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [HasRequiredRole]
    
    # Hang the sign above the door: Who is allowed here?
    required_roles = ['MANAGER', 'DELIVERY', ]



class CategoryView(viewsets.ModelViewSet): 
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOnly]



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    permission_classes = [HasRequiredRole]
    
    # as long as he is logged in he can Book
    required_roles = ['MANAGER', 'DELIVERY', 'CUSTOMER']
    


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()  
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # only ever return cart items that belong to THIS logged-in user's cart
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        # find this user's cart, or create one if they've never had a cart before
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        # attach it automatically — the client never sends a cart id
        serializer.save(cart=cart)



class OrderViewSet(viewsets.ModelViewSet):
    """
    Handles order creation (this is what the "Confirm Order" button posts to)
    plus standard retrieve/update/delete for a single order.
 
    Must be logged in. Non-managers only ever see/touch their own orders;
    managers can see everyone's — mirrors the OrderListView rules above.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()  # used by the router to infer the basename
 
    def get_queryset(self):
        qs = Order.objects.select_related("user").prefetch_related("items__item")
        return qs.filter(user=self.request.user)
 




# To fetch categories names:
class CategoryNameView(viewsets.ReadOnlyModelViewSet): 
    queryset = Category.objects.all()
    serializer_class = CategoryNameSerializer




###################
from collections import defaultdict
from django.db.models import F

 
class ConfirmOrderView(APIView):
    def post(self, request):
        user = request.user
 
        with transaction.atomic():
            cart_items = CartItem.objects.select_related("item").filter(cart__user=user)
 
            if not cart_items.exists():
                return Response(
                    {"error": "The basket is empty, the order cannot be confirmed."},
                    status=status.HTTP_400_BAD_REQUEST
                )
 
            # --- Lock the relevant MenuItems rows for this transaction ---
            item_ids = cart_items.values_list("item_id", flat=True)
            locked_menu_items = MenuItems.objects.select_for_update().filter(id__in=item_ids)
            stock_by_item_id = {mi.id: mi.inventory for mi in locked_menu_items}
            title_by_item_id = {mi.id: mi.title for mi in locked_menu_items}
 
            # --- Aggregate requested quantity per item (in case of dupes) ---
            requested_qty_by_item_id = defaultdict(int)
            for cart_item in cart_items:
                requested_qty_by_item_id[cart_item.item_id] += cart_item.quantity
 
            # --- Validate stock BEFORE creating anything ---
            insufficient = []
            for item_id, requested_qty in requested_qty_by_item_id.items():
                available = stock_by_item_id.get(item_id, 0)
                if requested_qty > available:
                    insufficient.append({
                        "item": title_by_item_id.get(item_id, f"item {item_id}"),
                        "requested": requested_qty,
                        "available": available,
                    })
 
            if insufficient:
                return Response(
                    {
                        "error": "Insufficient stock for one or more items in your basket.",
                        "details": insufficient,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
 
            # --- Everything is in stock: proceed as before ---
            total_price = sum(item.item.price * item.quantity for item in cart_items)
 
            order = Order.objects.create(
                user=user,
                total_price=total_price
            )
 
            order_items_to_create = []
            for cart_item in cart_items:
                order_items_to_create.append(
                    OrderItem(
                        order=order,
                        item=cart_item.item,
                        quantity=cart_item.quantity,
                        price_at_time=cart_item.item.price
                    )
                )
 
            OrderItem.objects.bulk_create(order_items_to_create)
 
            # --- Decrement stock atomically ---
            for item_id, requested_qty in requested_qty_by_item_id.items():
                MenuItems.objects.filter(id=item_id).update(
                    inventory=F("inventory") - requested_qty
                )
 
            cart_items.delete()
 
            return Response(
                {"message": "The product is effective and the demand is effective!", "order_id": order.id},
                status=status.HTTP_201_CREATED
            )
 


class OrderListView(APIView):
    """
    GET /api/orders/
 
    Query params (managers only):
        category               - filter by menu item category (case-insensitive)
        min_price / max_price  - filter by order total_price
        year / month / day / hour - filter by date_ordered components
    """
 
    # AllowAny at the view level because we need custom branching logic
    # (guest vs customer vs manager) rather than a single hard gate.
    permission_classes = [permissions.AllowAny]
 
    def get(self, request):
        user = request.user
 
        if not user.is_authenticated:
            return Response(
                {"detail": "You have to log in to see your orders."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
 
        if IsManagerOnly().has_permission(request, self):
            return self._manager_response(request)
 
        return self._customer_response(user)
 
    def _customer_response(self, user):
        orders = (
            Order.objects.filter(user=user)
            .select_related("user")
            .prefetch_related("items__item")
            .order_by("-date_ordered")
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(
            {"count": orders.count(), "orders": serializer.data},
            status=status.HTTP_200_OK,
        )
 
    def _manager_response(self, request):
        base_qs = (
            Order.objects.all()
            .select_related("user")
            .prefetch_related("items__item")
            .order_by("-date_ordered")
            .distinct()  # avoid duplicate rows from the items__item join
        )
        filtered_qs = OrderFilter(request.query_params, queryset=base_qs).qs
        serializer = UserRoleSerializer(filtered_qs, many=True)
        return Response(
            {"count": filtered_qs.count(), "orders": serializer.data},
            status=status.HTTP_200_OK,
        )



class ManagerDashboardView(APIView):


    """
    GET /api/dashboard/
 
    Success:
        200 OK
        {
            "count": 2,
            "orders": [
                {
                    "id": 1,
                    "user": "alice",
                    "items": [
                        {
                            "id": 5,
                            "item": {"id": 3, "title": "Cheeseburger", "price": "8.50", ...},
                            "quantity": 2,
                            "price_at_time": "8.50",
                            "subtotal": 17.00
                        }
                    ],
                    "items_count": 1,
                    "total_price": "17.00",
                    "date_ordered": "2026-07-09T14:32:10Z"
                },
                ...
            ]
        }
 
    Errors:
        401 Unauthorized -> raised for BOTH missing/invalid token and
                             authenticated-but-not-a-manager requests
                             (see permission_denied override below).
 
        Note: this is a read-only list endpoint with no request body and
        no single-resource lookup, so 400 (invalid input) and 404 (item
        not found) don't naturally apply here:
          - No orders yet -> still 200 OK with "orders": [] (standard
            REST convention: an empty collection is not an error).
          - If you later add query-string filters (e.g. ?date_from=...),
            validate those and return 400 with a message like
            "Invalid date_from format. Expected YYYY-MM-DD." on failure.
    """
 
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = [IsManagerOnly]
 
    def get(self, request):
        orders = (
            Order.objects
            .select_related("user")
            .prefetch_related("items__item")
            .order_by("-date_ordered")
        )
 
        serializer = OrderSerializer(orders, many=True)
 
        return Response(
            {
                "count": orders.count(),
                "orders": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
 





