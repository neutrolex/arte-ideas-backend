"""
Modelos relacionados con Usuarios
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuario del sistema con roles específicos para estudios fotográficos
    """
    ROLE_CHOICES = [
        ('super_admin', 'Super Administrador'),  # Ve todos los tenants
        ('admin', 'Administrador'),              # Admin del tenant
        ('manager', 'Gerente'),                  # Gerente del tenant
        ('employee', 'Empleado'),                # Empleado del tenant
        ('photographer', 'Fotógrafo'),           # Fotógrafo del tenant
        ('assistant', 'Asistente'),              # Asistente del tenant
    ]
    
    id = models.AutoField(primary_key=True)
    
    # Relación con tenant (null para super_admin)
    tenant = models.ForeignKey(
        'Tenant', 
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
        default='employee',
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
            'manager': [
                # Acceso a módulos (la mayoría)
                'access:dashboard', 'access:agenda', 'access:pedidos', 'access:clientes',
                'access:inventario', 'access:activos', 'access:produccion',
                'access:contratos', 'access:reportes',
                # Algunas acciones sensibles
                'view:margenes', 'view:datos_clientes', 'edit:precios'
            ],
            'employee': [
                # Acceso básico a módulos
                'access:dashboard', 'access:pedidos', 'access:clientes',
                'access:inventario', 'access:produccion',
                # Sin acciones sensibles
            ],
            'photographer': [
                # Acceso específico para fotógrafos
                'access:dashboard', 'access:agenda', 'access:pedidos', 'access:clientes',
                'access:produccion',
                # Sin acciones sensibles financieras
            ],
            'assistant': [
                # Acceso mínimo
                'access:dashboard', 'access:agenda', 'access:clientes',
                # Sin acciones sensibles
            ]
        }
        
        return permissions_map.get(self.role, [])
        
    def has_permission(self, permission):
        """Verificar si el usuario tiene un permiso específico"""
        return permission in self.get_permissions_list()


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
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE, verbose_name='Tenant')
    
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