from .serializers import  CartItemSerializer, OrderSerializer
from users.serializers import UserRoleSerializer
from .models import Cart, CartItem, Order, OrderItem
from menu.models import MenuItems
from rest_framework import viewsets
from users.permissions import IsManagerOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from collections import defaultdict
from django.db.models import F


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
 


