"""
Modelos del Core App - Arte Ideas
Sistema multi-tenant para estudios fotográficos

NOTA: Este archivo mantiene las importaciones para compatibilidad con migraciones existentes.
Los modelos han sido reorganizados en módulos específicos:
- autenticacion/models.py - Usuario y permisos
- usuarios/models.py - Perfiles y actividades de usuario  
- configuracion_sistema/models.py - Configuraciones globales
- multitenancy/models.py - Tenants y configuraciones específicas
"""

# Importar todos los modelos desde los nuevos módulos para mantener compatibilidad
from .autenticacion.models import User, RolePermission
from .usuarios.models import UserProfile, UserActivity
from .configuracion_sistema.models import SystemConfiguration
from .multitenancy.models import Tenant, TenantConfiguration

# Mantener las clases disponibles en este namespace para compatibilidad
__all__ = [
    'User', 'RolePermission', 'UserProfile', 'UserActivity',
    'SystemConfiguration', 'Tenant', 'TenantConfiguration'
]