from django.urls import path
from . import views
from rest_framework import routers

# Explicitly name the app to allow reverse lookups like 'restaurant:booking'
# In case there are same api end points in another app it won't be hard for django to tell the difference :)
app_name = 'restaurant'


urlpatterns = [
    path('', views.home_page, name='home'),


    path('menu/', views.menu_page, name='menu'),

    path('menu/<int:pk>/', views.menu_item_page, name='menu-item-detail'),

    path('menu/create/', views.menu_item_create, name='menu-item-create'),


    path('newcategory', views.create_category, name='create-category'),



    path('members/', views.members_page, name='members'),






    path('about/', views.about_page, name='abou'),

    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
]



