from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookings.views import BookingViewSet
from menu.views import MenuView, CategoryView, CategoryNameView
from orders.views import CartItemViewSet, OrderViewSet, ConfirmOrderView
from users.views import MembersDataAPI, ManagerDashboardView 

from django.conf import settings 
from django.conf.urls.static import static



router = DefaultRouter()
router.register(r'tables', BookingViewSet)
router.register(r'menu', MenuView)
router.register(r'categories', CategoryView)
router.register(r'category-names', CategoryNameView, basename='category-names')
router.register(r'cart-items', CartItemViewSet)
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'members-data', MembersDataAPI)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 3. Point your standard web pages to the new 'pages' app
    path('', include('pages.urls')),

    # Djoser authentication endpoints:
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    # Centralized API router
    path('api/', include(router.urls)),

    # Point these specific API paths to their imported views
    path('api/orders-confirmation/', ConfirmOrderView.as_view(), name='order-list'),
    path('api/dashboard/', ManagerDashboardView.as_view(), name='dashboard'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


