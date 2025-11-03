"""
Admin del Core App - Arte Ideas
Vista admin personalizada para mostrar funcionalidades al cliente
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Tenant, User, UserProfile, UserActivity, TenantConfiguration, RolePermission


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    """Admin para gestión de tenants"""
    list_display = ['name', 'business_name', 'location_type', 'currency', 'max_users', 'is_active', 'created_at']
    list_filter = ['location_type', 'currency', 'is_active', 'created_at']
    search_fields = ['name', 'business_name', 'business_email', 'business_ruc']
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'name', 'slug', 'description', 'is_active')
        }),
        ('Configuración del Negocio', {
            'fields': ('business_name', 'business_address', 'business_phone', 
                      'business_email', 'business_ruc', 'currency')
        }),
        ('Configuración del Tenant', {
            'fields': ('location_type', 'max_users', 'max_storage_mb')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Solo super admin puede crear tenants
        return request.user.is_superuser or request.user.role == 'super_admin'
    
    def has_change_permission(self, request, obj=None):
        # Solo super admin puede modificar tenants
        return request.user.is_superuser or request.user.role == 'super_admin'
    
    def has_delete_permission(self, request, obj=None):
        # Solo super admin puede eliminar tenants
        return request.user.is_superuser or request.user.role == 'super_admin'


class UserProfileInline(admin.StackedInline):
    """Inline para perfil de usuario"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fields = ['language', 'theme', 'email_notifications']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin personalizado para usuarios"""
    inlines = [UserProfileInline]
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'tenant', 'is_active', 'date_joined']
    list_filter = ['role', 'tenant', 'is_active', 'email_verified', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    readonly_fields = ['id', 'date_joined', 'last_login']
    
    fieldsets = (
        ('Información de Cuenta', {
            'fields': ('id', 'username', 'password', 'email', 'email_verified')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'phone', 'address', 'bio', 'avatar')
        }),
        ('Configuración del Sistema', {
            'fields': ('tenant', 'role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Estado de la Cuenta', {
            'fields': ('is_new_user', 'date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
        ('Permisos', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Información Básica', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'tenant', 'role'),
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'phone'),
        }),
    )
    
    def get_queryset(self, request):
        """Filtrar usuarios según permisos"""
        qs = super().get_queryset(request)
        
        if request.user.is_superuser or request.user.role == 'super_admin':
            # Super admin ve todos los usuarios
            return qs
        elif hasattr(request.user, 'tenant') and request.user.tenant:
            # Admin de tenant solo ve usuarios de su tenant
            return qs.filter(tenant=request.user.tenant)
        else:
            # Sin tenant, no ve usuarios
            return qs.none()
    
    def has_add_permission(self, request):
        # Solo admin puede crear usuarios
        return (request.user.is_superuser or 
                request.user.role in ['super_admin', 'admin'])
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'super_admin':
            return True
        if obj and request.user.role == 'admin':
            return obj.tenant == request.user.tenant
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'super_admin':
            return True
        if obj and request.user.role == 'admin':
            return obj.tenant == request.user.tenant
        return False


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin para actividad de usuarios"""
    list_display = ['user', 'tenant', 'action', 'module', 'description', 'created_at']
    list_filter = ['action', 'module', 'tenant', 'created_at']
    search_fields = ['user__username', 'user__email', 'description']
    readonly_fields = ['user', 'tenant', 'action', 'description', 'module', 
                      'ip_address', 'user_agent', 'created_at']
    
    def get_queryset(self, request):
        """Filtrar actividad según permisos"""
        qs = super().get_queryset(request)
        
        if request.user.is_superuser or request.user.role == 'super_admin':
            return qs
        elif hasattr(request.user, 'tenant') and request.user.tenant:
            return qs.filter(tenant=request.user.tenant)
        else:
            return qs.none()
    
    def has_add_permission(self, request):
        return False  # No se crean manualmente
    
    def has_change_permission(self, request, obj=None):
        return False  # Solo lectura
    
    def has_delete_permission(self, request, obj=None):
        # Solo super admin puede eliminar logs
        return request.user.is_superuser or request.user.role == 'super_admin'


@admin.register(TenantConfiguration)
class TenantConfigurationAdmin(admin.ModelAdmin):
    """Admin para configuraciones por tenant"""
    list_display = ['tenant', 'module', 'key', 'value', 'data_type', 'is_editable']
    list_filter = ['tenant', 'module', 'data_type', 'is_editable']
    search_fields = ['tenant__name', 'key', 'value', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Configuración', {
            'fields': ('tenant', 'module', 'key', 'value', 'data_type')
        }),
        ('Metadatos', {
            'fields': ('description', 'is_editable', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Filtrar configuraciones según permisos"""
        qs = super().get_queryset(request)
        
        if request.user.is_superuser or request.user.role == 'super_admin':
            return qs
        elif hasattr(request.user, 'tenant') and request.user.tenant:
            return qs.filter(tenant=request.user.tenant)
        else:
            return qs.none()
    
    def has_add_permission(self, request):
        return request.user.role in ['super_admin', 'admin']
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'super_admin':
            return True
        if obj and request.user.role == 'admin':
            return obj.tenant == request.user.tenant
        return False


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """Admin para permisos por rol"""
    list_display = ['tenant', 'role', 'modules_enabled', 'sensitive_actions_enabled']
    list_filter = ['tenant', 'role']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Configuración Básica', {
            'fields': ('tenant', 'role')
        }),
        ('Acceso a Módulos', {
            'fields': ('access_dashboard', 'access_agenda', 'access_pedidos', 'access_clientes',
                      'access_inventario', 'access_activos', 'access_gastos', 'access_produccion',
                      'access_contratos', 'access_reportes'),
            'classes': ('collapse',)
        }),
        ('Acciones Sensibles', {
            'fields': ('view_costos', 'view_precios', 'view_margenes', 'view_datos_clientes',
                      'view_datos_financieros', 'edit_precios', 'delete_registros'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def modules_enabled(self, obj):
        """Mostrar cantidad de módulos habilitados"""
        modules = [
            obj.access_dashboard, obj.access_agenda, obj.access_pedidos,
            obj.access_clientes, obj.access_inventario, obj.access_activos,
            obj.access_gastos, obj.access_produccion, obj.access_contratos,
            obj.access_reportes
        ]
        enabled = sum(modules)
        return f"{enabled}/10"
    modules_enabled.short_description = "Módulos Habilitados"
    
    def sensitive_actions_enabled(self, obj):
        """Mostrar cantidad de acciones sensibles habilitadas"""
        actions = [
            obj.view_costos, obj.view_precios, obj.view_margenes,
            obj.view_datos_clientes, obj.view_datos_financieros,
            obj.edit_precios, obj.delete_registros
        ]
        enabled = sum(actions)
        return f"{enabled}/7"
    sensitive_actions_enabled.short_description = "Acciones Sensibles"
    
    def get_queryset(self, request):
        """Filtrar permisos según tenant"""
        qs = super().get_queryset(request)
        
        if request.user.is_superuser or request.user.role == 'super_admin':
            return qs
        elif hasattr(request.user, 'tenant') and request.user.tenant:
            return qs.filter(tenant=request.user.tenant)
        else:
            return qs.none()
    
    def has_add_permission(self, request):
        return request.user.role in ['super_admin', 'admin']
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'super_admin':
            return True
        if obj and request.user.role == 'admin':
            return obj.tenant == request.user.tenant
        return False


# Personalización del admin site
admin.site.site_header = "Arte Ideas - Administración"
admin.site.site_title = "Arte Ideas Admin"
admin.site.index_title = "Panel de Administración"


# Acción personalizada para cambiar contexto de tenant (solo super admin)
def switch_tenant_context(modeladmin, request, queryset):
    """Acción para cambiar contexto de tenant"""
    if request.user.role != 'super_admin':
        messages.error(request, "Solo super admin puede cambiar contexto de tenant")
        return
    
    if queryset.count() != 1:
        messages.error(request, "Selecciona exactamente un tenant")
        return
    
    tenant = queryset.first()
    # Aquí se implementaría la lógica para cambiar contexto
    # Por ahora solo mostramos un mensaje
    messages.success(request, f"Contexto cambiado a: {tenant.name}")

switch_tenant_context.short_description = "Cambiar contexto de tenant"

# Agregar la acción al admin de Tenant
TenantAdmin.actions = [switch_tenant_context]