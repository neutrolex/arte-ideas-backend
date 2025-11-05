"""
URLs del Commerce App - Arte Ideas
Configuración de rutas para el módulo de pedidos
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, OrderItemViewSet, ProductViewSet

app_name = 'commerce'

# Crear router principal
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Rutas del router principal
    path('', include(router.urls)),
    
    # Rutas personalizadas para funciones específicas
    path('orders/summary/', OrderViewSet.as_view({'get': 'summary'}), name='order-summary'),
    path('orders/totals_summary/', OrderViewSet.as_view({'get': 'totals_summary'}), name='order-totals-summary'),
    path('orders/autocomplete-clients/', OrderViewSet.as_view({'get': 'autocomplete_clients'}), name='order-autocomplete-clients'),
    path('orders/overdue/', OrderViewSet.as_view({'get': 'overdue_orders'}), name='order-overdue'),
    path('orders/upcoming-deliveries/', OrderViewSet.as_view({'get': 'upcoming_deliveries'}), name='order-upcoming-deliveries'),
    path('orders/by-status/', OrderViewSet.as_view({'get': 'by_status'}), name='order-by-status'),
    
    # Rutas para acciones individuales de pedidos
    path('orders/<int:pk>/mark-completed/', OrderViewSet.as_view({'post': 'mark_as_completed'}), name='order-mark-completed'),
    path('orders/<int:pk>/mark-cancelled/', OrderViewSet.as_view({'post': 'mark_as_cancelled'}), name='order-mark-cancelled'),
    
    # Rutas para productos
    path('products/low-stock/', ProductViewSet.as_view({'get': 'low_stock'}), name='product-low-stock'),
    path('products/active/', ProductViewSet.as_view({'get': 'active_products'}), name='product-active'),
    path('products/<int:pk>/update-stock/', ProductViewSet.as_view({'post': 'update_stock'}), name='product-update-stock'),
]