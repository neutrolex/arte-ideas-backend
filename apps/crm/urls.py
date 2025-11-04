"""
URLs del CRM App - Arte Ideas
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.crm.clientes.views import ClienteViewSet
from apps.crm.contracts.views import ContractViewSet

app_name = 'crm'

# Router para ViewSets
router = DefaultRouter()
router.register(r'clients', ClienteViewSet, basename='clients')
router.register(r'contracts', ContractViewSet, basename='contracts')

urlpatterns = [
    # API Router
    path('', include(router.urls)),
]