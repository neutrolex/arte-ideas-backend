"""
URLs del Operations App - Arte Ideas
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'operations'

# Router para ViewSets
router = DefaultRouter()

urlpatterns = [
    # API Router
    path('', include(router.urls)),
    
    # Incluir URLs de la app de producción
    path('', include('apps.operations.produccion.urls')),
]