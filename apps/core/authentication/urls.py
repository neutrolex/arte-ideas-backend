"""
URLs del Módulo de Autenticación - Arte Ideas
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView

app_name = 'authentication'

urlpatterns = [
    # Autenticación JWT
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    
    # Logout
    path('logout/', LogoutView.as_view(), name='logout'),
]