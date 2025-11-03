"""
Modelos del Sistema (Configuraciones y Permisos)
"""
from django.db import models


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


class RolePermission(models.Model):
    """
    Permisos específicos por rol y tenant
    """
    ROLE_CHOICES = [
        ('super_admin', 'Super Administrador'),
        ('admin', 'Administrador'),
        ('manager', 'Gerente'),
        ('employee', 'Empleado'),
        ('photographer', 'Fotógrafo'),
        ('assistant', 'Asistente'),
    ]
    
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE, verbose_name='Tenant')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='Rol')
    
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
            'manager': {
                'access_dashboard': True, 'access_agenda': True, 'access_pedidos': True,
                'access_clientes': True, 'access_inventario': True, 'access_activos': True,
                'access_produccion': True, 'access_contratos': True, 'access_reportes': True,
                'view_margenes': True, 'view_datos_clientes': True, 'edit_precios': True
            },
            'employee': {
                'access_dashboard': True, 'access_pedidos': True, 'access_clientes': True,
                'access_inventario': True, 'access_produccion': True
            },
            'photographer': {
                'access_dashboard': True, 'access_agenda': True, 'access_pedidos': True,
                'access_clientes': True, 'access_produccion': True
            },
            'assistant': {
                'access_dashboard': True, 'access_agenda': True, 'access_clientes': True
            }
        }
        
        return defaults.get(role, {})