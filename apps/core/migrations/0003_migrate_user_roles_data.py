# Generated migration for role data migration
from django.db import migrations


def migrate_user_roles_forward(apps, schema_editor):
    """
    Migrar roles de usuarios de los antiguos a los nuevos según HU01
    """
    User = apps.get_model('core', 'User')
    RolePermission = apps.get_model('core', 'RolePermission')
    
    # Mapeo de roles antiguos a nuevos
    role_mapping = {
        'manager': 'admin',      # Gerentes se convierten en administradores
        'employee': 'ventas',    # Empleados se convierten en ventas (rol por defecto)
        'photographer': 'produccion',  # Fotógrafos se convierten en producción
        'assistant': 'operario', # Asistentes se convierten en operarios
        # super_admin y admin se mantienen igual
    }
    
    # Actualizar usuarios
    for old_role, new_role in role_mapping.items():
        User.objects.filter(role=old_role).update(role=new_role)
        print(f"Migrated users from {old_role} to {new_role}")
    
    # Actualizar permisos de roles - manejar duplicados
    for old_role, new_role in role_mapping.items():
        # Obtener registros que se van a migrar
        old_permissions = RolePermission.objects.filter(role=old_role)
        
        for old_perm in old_permissions:
            # Verificar si ya existe un registro con el nuevo rol para el mismo tenant
            existing = RolePermission.objects.filter(
                tenant=old_perm.tenant, 
                role=new_role
            ).first()
            
            if existing:
                # Si existe, eliminar el registro antiguo
                old_perm.delete()
                print(f"Removed duplicate role permission {old_role} for tenant {old_perm.tenant.id}")
            else:
                # Si no existe, actualizar el rol
                old_perm.role = new_role
                old_perm.save()
                print(f"Migrated role permission from {old_role} to {new_role} for tenant {old_perm.tenant.id}")


def migrate_user_roles_reverse(apps, schema_editor):
    """
    Migración reversa para restaurar roles antiguos
    """
    User = apps.get_model('core', 'User')
    RolePermission = apps.get_model('core', 'RolePermission')
    
    # Mapeo reverso (aproximado, puede haber pérdida de información)
    reverse_mapping = {
        'admin': 'manager',      # Algunos admin pueden haber sido manager
        'ventas': 'employee',    # Ventas vuelve a employee
        'produccion': 'photographer',  # Producción vuelve a photographer
        'operario': 'assistant', # Operario vuelve a assistant
    }
    
    # Solo migrar si no son admin originales
    for new_role, old_role in reverse_mapping.items():
        if new_role != 'admin':  # No tocar admin originales
            User.objects.filter(role=new_role).update(role=old_role)
            RolePermission.objects.filter(role=new_role).update(role=old_role)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_update_user_roles_hu01'),
    ]

    operations = [
        migrations.RunPython(
            migrate_user_roles_forward,
            migrate_user_roles_reverse,
        ),
    ]