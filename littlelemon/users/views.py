from .serializers import UserRoleSerializer
from .models import CustomUser
from rest_framework import viewsets
from .permissions import IsManagerOnly
from orders.serializers import OrderSerializer
from orders.models import Order
from orders.filters import OrderFilter
from users.permissions import IsManagerOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status




# because of DefaultRouter i don't need to create another view for single item view " he creates it for me :) "

# He can See the menu items (all can do it) + create/delete/patch/put menu items (if he is the manager or the )


class MembersDataAPI(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsManagerOnly]


    

class ManagerDashboardView(APIView):
    """
    GET /api/dashboard/
    Returns a count of orders and the order list.
    Supports query string filtering via OrderFilter.
    """
    permission_classes = [IsManagerOnly]
 
    def get(self, request):
        # 1. Build the base optimized query with distinct()
        base_qs = (
            Order.objects.all()
            .select_related("user")
            .prefetch_related("items__item")
            .order_by("-date_ordered")
            .distinct() 
        )
        
        # 2. Apply the filters from the request
        filtered_qs = OrderFilter(request.query_params, queryset=base_qs).qs
 
        # 3. Serialize the filtered data
        serializer = OrderSerializer(filtered_qs, many=True)
 
        # 4. Return the custom dictionary payload
        return Response(
            {
                "count": filtered_qs.count(),
                "orders": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


