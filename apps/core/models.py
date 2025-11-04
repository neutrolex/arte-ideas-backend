"""
Modelos del Core App - Arte Ideas
Sistema multi-tenant para estudios fotográficos
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class Tenant(models.Model):
    """
    Modelo para estudios fotográficos (tenants)
    Cada tenant representa un estudio fotográfico independiente
    """
    # Usar AutoField simple para testing fácil
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Nombre del Estudio')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Identificador')
    description = models.TextField(blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Configuración específica por tenant
    max_users = models.IntegerField(default=10, verbose_name='Máximo de Usuarios')
    max_storage_mb = models.IntegerField(default=1000, verbose_name='Almacenamiento Máximo (MB)')
    
    # Configuración del negocio (datos que se ven en la imagen)
    business_name = models.CharField(max_length=200, verbose_name='Nombre de la Empresa')
    business_address = models.TextField(verbose_name='Dirección')
    business_phone = models.CharField(max_length=15, verbose_name='Teléfono')
    business_email = models.EmailField(verbose_name='Email Corporativo')
    business_ruc = models.CharField(max_length=11, verbose_name='RUC')
    currency = models.CharField(
        max_length=10,
        choices=[
            ('PEN', 'Soles (S/)'),
            ('USD', 'Dólares ($)'),
            ('EUR', 'Euros (€)'),
        ],
        default='PEN',
        verbose_name='Moneda'
    )
    
    # Configuraciones de acceso (restricciones por ubicación)
    location_type = models.CharField(
        max_length=20,
        choices=[
            ('lima', 'Lima - Acceso Completo'),
            ('provincia', 'Provincia - Acceso Limitado'),
        ],
        default='lima',
        verbose_name='Tipo de Ubicación'
    )
    
    class Meta:
        verbose_name = 'Estudio Fotográfico'
        verbose_name_plural = 'Estudios Fotográficos'
        
    def __str__(self):
        return f"{self.name}"
        
    def save(self, *args, **kwargs):
        # Generar slug automáticamente si no existe
        if not self.slug:
            import re
            self.slug = re.sub(r'[^a-zA-Z0-9]', '', self.name.lower())[:50]
        super().save(*args, **kwargs)
        
    def has_global_data_access(self):
        """Verificar si el tenant tiene acceso a datos globales"""
        return self.location_type == 'lima'
        
    def has_financial_modules(self):
        """Verificar si el tenant tiene acceso a módulos financieros"""
        return self.location_type == 'lima'


class User(AbstractUser):
    """
    Usuario del sistema con roles específicos para estudios fotográficos
    """
    ROLE_CHOICES = [
        ('super_admin', 'Super Administrador'),  # Ve todos los tenants
        ('admin', 'Administrador'),              # Admin del tenant
        ('ventas', 'Ventas'),                    # Usuario de ventas
        ('produccion', 'Producción'),            # Usuario de producción
        ('operario', 'Operario'),                # Usuario operario
    ]
    
    id = models.AutoField(primary_key=True)
    
    # Relación con tenant (null para super_admin)
    tenant = models.ForeignKey(
        Tenant, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name='Estudio Fotográfico'
    )
    
    # Información adicional
    phone = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='operario',
        verbose_name='Rol'
    )
    
    # Control de cuenta
    is_new_user = models.BooleanField(default=True, verbose_name='Usuario Nuevo')
    email_verified = models.BooleanField(default=False, verbose_name='Email Verificado')
    
    # Información adicional del perfil
    address = models.TextField(blank=True, verbose_name='Dirección')
    bio = models.TextField(blank=True, verbose_name='Biografía')
    
    # Fechas importantes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
        
    def get_permissions_list(self):
        """
        Obtener lista de permisos según el rol
        Basado en la imagen de roles y permisos
        """
        permissions_map = {
            'super_admin': [
                # Acceso a módulos
                'access:dashboard', 'access:agenda', 'access:pedidos', 'access:clientes',
                'access:inventario', 'access:activos', 'access:gastos', 'access:produccion',
                'access:contratos', 'access:reportes', 'access:configuration',
                # Acciones sensibles
                'view:costos', 'view:precios', 'view:margenes', 'view:datos_clientes',
                'view:datos_financieros', 'edit:precios', 'delete:registros',
                # Gestión de usuarios y tenants
                'manage:users', 'manage:tenants', 'manage:permissions'
            ],
            'admin': [
                # Acceso a módulos (todos)
                'access:dashboard', 'access:agenda', 'access:pedidos', 'access:clientes',
                'access:inventario', 'access:activos', 'access:gastos', 'access:produccion',
                'access:contratos', 'access:reportes', 'access:configuration',
                # Acciones sensibles (todas)
                'view:costos', 'view:precios', 'view:margenes', 'view:datos_clientes',
                'view:datos_financieros', 'edit:precios', 'delete:registros',
                # Gestión dentro del tenant
                'manage:users', 'manage:permissions'
            ],
            'ventas': [
                # Acceso a módulos de ventas
                'access:dashboard', 'access:agenda', 'access:pedidos', 'access:clientes',
                'access:contratos', 'access:reportes',
                # Acciones específicas de ventas
                'view:datos_clientes', 'view:precios'
            ],
            'produccion': [
                # Acceso a módulos de producción
                'access:dashboard', 'access:produccion', 'access:inventario', 'access:activos',
                'access:pedidos', 'access:reportes',
                # Acciones específicas de producción
                'view:costos', 'view:inventario'
            ],
            'operario': [
                # Acceso básico operacional
                'access:dashboard', 'access:agenda', 'access:produccion',
                # Solo acceso de visualización básica
            ]
        }
        
        return permissions_map.get(self.role, [])
        
    def has_permission(self, permission):
        """Verificar si el usuario tiene un permiso específico"""
        return permission in self.get_permissions_list()


class SystemConfiguration(models.Model):
    """
    Configuraciones globales del sistema (compartidas entre tenants)
    """
    key = models.CharField(max_length=100, unique=True, verbose_name='Clave')
    value = models.TextField(verbose_name='Valor')
    description = models.TextField(blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuración del Sistema'
        verbose_name_plural = 'Configuraciones del Sistema'
        
    def __str__(self):
        return f"{self.key}: {self.value[:50]}"


class UserProfile(models.Model):
    """
    Perfil extendido del usuario (datos adicionales)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Preferencias del usuario
    language = models.CharField(
        max_length=10,
        choices=[
            ('es', 'Español'),
            ('en', 'English'),
        ],
        default='es',
        verbose_name='Idioma'
    )
    theme = models.CharField(
        max_length=10,
        choices=[
            ('light', 'Claro'),
            ('dark', 'Oscuro'),
        ],
        default='light',
        verbose_name='Tema'
    )
    
    # Configuraciones de notificaciones
    email_notifications = models.BooleanField(default=True, verbose_name='Notificaciones Email')
    
    # Estadísticas (calculadas dinámicamente)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
        
    def __str__(self):
        return f"Perfil de {self.user.get_full_name()}"


class UserActivity(models.Model):
    """
    Registro de actividad del usuario
    """
    ACTION_CHOICES = [
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
        ('create', 'Crear registro'),
        ('update', 'Actualizar registro'),
        ('delete', 'Eliminar registro'),
        ('export', 'Exportar datos'),
        ('config_change', 'Cambio de configuración'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Tenant')
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='Acción')
    description = models.TextField(verbose_name='Descripción')
    module = models.CharField(max_length=50, blank=True, verbose_name='Módulo')
    
    # Metadatos
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='Dirección IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Actividad de Usuario'
        verbose_name_plural = 'Actividades de Usuario'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.created_at}"


class TenantConfiguration(models.Model):
    """
    Configuraciones específicas por tenant
    """
    MODULE_CHOICES = [
        ('general', 'General'),
        ('crm', 'CRM'),
        ('commerce', 'Commerce'),
        ('operations', 'Operations'),
        ('finance', 'Finance'),
        ('analytics', 'Analytics'),
    ]
    
    DATA_TYPE_CHOICES = [
        ('string', 'Texto'),
        ('integer', 'Número entero'),
        ('float', 'Número decimal'),
        ('boolean', 'Verdadero/Falso'),
        ('json', 'JSON'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Tenant')
    module = models.CharField(max_length=20, choices=MODULE_CHOICES, verbose_name='Módulo')
    key = models.CharField(max_length=100, verbose_name='Clave')
    value = models.TextField(verbose_name='Valor')
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES, default='string', verbose_name='Tipo de dato')
    description = models.TextField(blank=True, verbose_name='Descripción')
    
    # Metadatos
    is_editable = models.BooleanField(default=True, verbose_name='Editable')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuración del Tenant'
        verbose_name_plural = 'Configuraciones del Tenant'
        unique_together = ['tenant', 'module', 'key']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.module}.{self.key}"
    
    def get_typed_value(self):
        """Obtener el valor con el tipo de dato correcto"""
        if self.data_type == 'integer':
            return int(self.value)
        elif self.data_type == 'float':
            return float(self.value)
        elif self.data_type == 'boolean':
            return self.value.lower() in ['true', '1', 'yes']
        elif self.data_type == 'json':
            import json
            return json.loads(self.value)
        return self.value


class RolePermission(models.Model):
    """
    Permisos específicos por rol y tenant
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Tenant')
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES, verbose_name='Rol')
    
    # Módulos con acceso
    access_dashboard = models.BooleanField(default=True, verbose_name='Dashboard')
    access_agenda = models.BooleanField(default=True, verbose_name='Agenda')
    access_pedidos = models.BooleanField(default=True, verbose_name='Pedidos')
    access_clientes = models.BooleanField(default=True, verbose_name='Clientes')
    access_inventario = models.BooleanField(default=False, verbose_name='Inventario')
    access_activos = models.BooleanField(default=False, verbose_name='Activos')
    access_gastos = models.BooleanField(default=False, verbose_name='Gastos')
    access_produccion = models.BooleanField(default=False, verbose_name='Producción')
    access_contratos = models.BooleanField(default=False, verbose_name='Contratos')
    access_reportes = models.BooleanField(default=False, verbose_name='Reportes')
    
    # Acciones sensibles
    view_costos = models.BooleanField(default=False, verbose_name='Ver Costos')
    view_precios = models.BooleanField(default=False, verbose_name='Ver Precios')
    view_margenes = models.BooleanField(default=False, verbose_name='Ver Márgenes')
    view_datos_clientes = models.BooleanField(default=False, verbose_name='Ver Datos de Clientes')
    view_datos_financieros = models.BooleanField(default=False, verbose_name='Ver Datos Financieros')
    edit_precios = models.BooleanField(default=False, verbose_name='Editar Precios')
    delete_registros = models.BooleanField(default=False, verbose_name='Eliminar Registros')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Permiso de Rol'
        verbose_name_plural = 'Permisos de Roles'
        unique_together = ['tenant', 'role']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.get_role_display()}"
    
    @classmethod
    def get_default_permissions(cls, role):
        """Obtener permisos por defecto para un rol"""
        defaults = {
            'super_admin': {
                'access_dashboard': True, 'access_agenda': True, 'access_pedidos': True,
                'access_clientes': True, 'access_inventario': True, 'access_activos': True,
                'access_gastos': True, 'access_produccion': True, 'access_contratos': True,
                'access_reportes': True, 'view_costos': True, 'view_precios': True,
                'view_margenes': True, 'view_datos_clientes': True, 'view_datos_financieros': True,
                'edit_precios': True, 'delete_registros': True
            },
            'admin': {
                'access_dashboard': True, 'access_agenda': True, 'access_pedidos': True,
                'access_clientes': True, 'access_inventario': True, 'access_activos': True,
                'access_gastos': True, 'access_produccion': True, 'access_contratos': True,
                'access_reportes': True, 'view_costos': True, 'view_precios': True,
                'view_margenes': True, 'view_datos_clientes': True, 'view_datos_financieros': True,
                'edit_precios': True, 'delete_registros': True
            },
            'ventas': {
                'access_dashboard': True, 'access_agenda': True, 'access_pedidos': True,
                'access_clientes': True, 'access_contratos': True, 'access_reportes': True,
                'view_datos_clientes': True, 'view_precios': True
            },
            'produccion': {
                'access_dashboard': True, 'access_produccion': True, 'access_inventario': True,
                'access_activos': True, 'access_pedidos': True, 'access_reportes': True,
                'view_costos': True
            },
            'operario': {
                'access_dashboard': True, 'access_agenda': True, 'access_produccion': True
            }
        }
        return defaults.get(role, {})