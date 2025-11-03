"""
URLs del Core App - Arte Ideas
Estructura modular organizada por subcarpetas
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoreHealthCheckView

app_name = 'core'

# Router para ViewSets
router = DefaultRouter()

urlpatterns = [
    # API Router
    path('', include(router.urls)),
    
    # Health Check
    path('health/', CoreHealthCheckView.as_view(), name='health_check'),
    
    # Módulo Autenticación
    path('auth/', include('apps.core.authentication.urls')),
    
    # Módulo Mi Perfil
    path('profile/', include('apps.core.profile.urls')),
    
    # Módulo Configuración
    path('config/', include('apps.core.configuration.urls')),
]