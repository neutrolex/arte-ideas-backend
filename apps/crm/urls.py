"""
URLs del CRM App - Arte Ideas
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ContratoViewSet

app_name = 'crm'

# Router principal
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'contratos', ContratoViewSet, basename='contratos')

urlpatterns = [
    # API Router principal
    path('', include(router.urls)),
    
    # Submódulo Contratos (mantenido por compatibilidad)
    path('contracts/', include('apps.crm.contracts.urls')),
    
    # Submódulo Agenda
    path('agenda/', include('apps.crm.agenda.urls')),
]