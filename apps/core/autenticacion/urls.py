"""
URLs del Módulo de Autenticación - Arte Ideas
"""
from django.urls import path
from .views import LogoutView

app_name = 'autenticacion'

urlpatterns = [
    # Autenticación
    path('logout/', LogoutView.as_view(), name='logout'),
]