from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant import views 



router = DefaultRouter()
router.register(r'tables', views.BookingViewSet)
router.register(r'menu', views.MenuView)
router.register(r'categories', views.CategoryView)

router.register(r'category-names', views.CategoryNameView, basename='category-names')

router.register(r'cart-items', views.CartItemViewSet)

router.register(r'orders', views.OrderViewSet, basename='order')

router.register(r'members-data', views.MembersDataAPI)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurant.urls')),


    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include(router.urls)),
 

    # path('api/confirm-order/', views.ConfirmOrderView.as_view(), name='confirm-order'),

    path('api/orders-confirmation/', views.ConfirmOrderView.as_view(), name='order-list'),

    path('api/dashboard/', views.ManagerDashboardView.as_view(), name='dashboard'),

]


