from django.shortcuts import render
from .serializers import BookingSerializer, MenuSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer, UserRoleSerializer, CategorySerializer
from .models import Booking, MenuItems, Cart, CartItem, Order, OrderItem, CustomUser, Category
from rest_framework import viewsets
from .permissions import HasRequiredRole, IsManagerOnly




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
    


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer



class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

 

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer






