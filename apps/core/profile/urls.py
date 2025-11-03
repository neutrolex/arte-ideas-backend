"""
URLs del Módulo Mi Perfil - Arte Ideas
"""
from django.urls import path
from .views import (
    ProfileView, ProfileStatisticsView, ProfileActivityView,
    ProfileCompletionView, ChangePasswordView, ChangeEmailView
)

app_name = 'profile'

urlpatterns = [
    # Mi Perfil - Datos básicos
    path('view/', ProfileView.as_view(), name='profile_view'),           # GET - Ver perfil
    path('edit/', ProfileView.as_view(), name='profile_edit'),           # PUT - Editar perfil
    
    # Mi Perfil - Información adicional
    path('statistics/', ProfileStatisticsView.as_view(), name='statistics'),     # GET - Estadísticas
    path('activity/', ProfileActivityView.as_view(), name='activity'),           # GET - Actividad
    path('completion/', ProfileCompletionView.as_view(), name='completion'),     # GET - Completitud
    
    # Mi Perfil - Seguridad
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),  # POST - Cambiar contraseña
    path('change-email/', ChangeEmailView.as_view(), name='change_email'),          # POST - Cambiar email
]