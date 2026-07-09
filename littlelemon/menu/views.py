from django.shortcuts import render
from .serializers import MenuSerializer, CategorySerializer, CategoryNameSerializer
from .models import MenuItems, Category
from rest_framework import viewsets
from users.permissions import HasRequiredRole, IsManagerOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


# because of DefaultRouter i don't need to create another view for single item view " he creates it for me :) "
class MenuView(viewsets.ModelViewSet): 
    queryset = MenuItems.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [HasRequiredRole]
    
    # Hang the sign above the door: Who is allowed here?
    required_roles = ['MANAGER', 'DELIVERY']

    # 2. Tell your view to use these parsers
    parser_classes = [MultiPartParser, FormParser, JSONParser]


class CategoryView(viewsets.ModelViewSet): 
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOnly]


# To fetch categories names:
class CategoryNameView(viewsets.ReadOnlyModelViewSet): 
    queryset = Category.objects.all()
    serializer_class = CategoryNameSerializer





