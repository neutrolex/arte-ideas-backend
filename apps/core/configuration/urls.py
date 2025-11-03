"""
URLs del Módulo Configuración - Arte Ideas
"""
from django.urls import path
from .views import (
    BusinessConfigurationView, UsersManagementView, UserManagementDetailView,
    RolePermissionsView, RolesListView, TenantsManagementView, TenantUsersView
)

app_name = 'configuration'

urlpatterns = [
    # Configuración del Negocio
    path('business/view/', BusinessConfigurationView.as_view(), name='business_view'),    # GET - Ver configuración
    path('business/edit/', BusinessConfigurationView.as_view(), name='business_edit'),    # PUT - Editar configuración
    
    # Gestión de Usuarios
    path('users/list/', UsersManagementView.as_view(), name='users_list'),               # GET - Lista usuarios
    path('users/create/', UsersManagementView.as_view(), name='users_create'),           # POST - Crear usuario
    path('users/<int:user_id>/view/', UserManagementDetailView.as_view(), name='user_view'),     # GET - Ver usuario
    path('users/<int:user_id>/edit/', UserManagementDetailView.as_view(), name='user_edit'),     # PUT - Editar usuario
    path('users/<int:user_id>/toggle/', UserManagementDetailView.as_view(), name='user_toggle'), # PATCH - Activar/Desactivar
    path('users/<int:user_id>/delete/', UserManagementDetailView.as_view(), name='user_delete'), # DELETE - Eliminar usuario
    
    # Roles y Permisos
    path('roles/list/', RolesListView.as_view(), name='roles_list'),                     # GET - Lista roles
    path('permissions/<str:role>/view/', RolePermissionsView.as_view(), name='permissions_view'),   # GET - Ver permisos
    path('permissions/<str:role>/edit/', RolePermissionsView.as_view(), name='permissions_edit'),   # PUT - Editar permisos
    path('permissions/<str:role>/reset/', RolePermissionsView.as_view(), name='permissions_reset'), # POST - Restablecer
    
    # Super Admin - Gestión de Tenants
    path('tenants/list/', TenantsManagementView.as_view(), name='tenants_list'),         # GET - Lista tenants
    path('tenants/create/', TenantsManagementView.as_view(), name='tenants_create'),     # POST - Crear tenant
    path('tenants/<int:tenant_id>/users/', TenantUsersView.as_view(), name='tenant_users'), # GET - Usuarios del tenant
]