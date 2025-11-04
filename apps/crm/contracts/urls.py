"""
URLs del módulo Contratos (CRM)
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContractViewSet

app_name = 'contracts'

# Router para ViewSets
router = DefaultRouter()
# Prefijo vacío para exponer /api/contracts/ directamente
router.register(r'', ContractViewSet, basename='contracts')

urlpatterns = [
    # API Router
    path('', include(router.urls)),
]