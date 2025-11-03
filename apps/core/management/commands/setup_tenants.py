"""
Comando para crear datos de prueba para tenants A y B
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import Tenant, RolePermission, TenantConfiguration, UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Crear tenants de prueba A y B con usuarios y configuraciones'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando tenants de prueba...'))
        
        # Crear Tenant A (Lima - Acceso completo)
        tenant_a, created = Tenant.objects.get_or_create(
            slug='tenant-a',
            defaults={
                'name': 'Estudio Fotográfico A',
                'business_name': 'Arte Ideas Diseño Gráfico A',
                'business_address': 'Av. Lima 123, San Juan de Lurigancho',
                'business_phone': '987654321',
                'business_email': 'info@tenant-a.com',
                'business_ruc': '20123456789',
                'currency': 'PEN',
                'location_type': 'lima',
                'max_users': 20,
                'max_storage_mb': 2000,
            }
        )
        if created:
            self.stdout.write(f'✓ Tenant A creado: {tenant_a.name}')
        else:
            self.stdout.write(f'✓ Tenant A ya existe: {tenant_a.name}')
        
        # Crear Tenant B (Provincia - Acceso limitado)
        tenant_b, created = Tenant.objects.get_or_create(
            slug='tenant-b',
            defaults={
                'name': 'Estudio Fotográfico B',
                'business_name': 'Arte Ideas Diseño Gráfico B',
                'business_address': 'Av. Arequipa 456, Cusco',
                'business_phone': '987654322',
                'business_email': 'info@tenant-b.com',
                'business_ruc': '20987654321',
                'currency': 'PEN',
                'location_type': 'provincia',
                'max_users': 10,
                'max_storage_mb': 1000,
            }
        )
        if created:
            self.stdout.write(f'✓ Tenant B creado: {tenant_b.name}')
        else:
            self.stdout.write(f'✓ Tenant B ya existe: {tenant_b.name}')
        
        # Crear Super Admin (acceso a ambos tenants)
        super_admin, created = User.objects.get_or_create(
            username='superadmin',
            defaults={
                'email': 'admin@arteideas.com',
                'first_name': 'Super',
                'last_name': 'Administrador',
                'role': 'super_admin',
                'tenant': None,  # Super admin no pertenece a un tenant específico
                'is_staff': True,
                'is_superuser': True,
                'email_verified': True,
                'is_new_user': False,
            }
        )
        if created:
            super_admin.set_password('admin123')
            super_admin.save()
            self.stdout.write(f'✓ Super Admin creado: {super_admin.username}')
        else:
            self.stdout.write(f'✓ Super Admin ya existe: {super_admin.username}')
        
        # Crear usuarios para Tenant A
        admin_a, created = User.objects.get_or_create(
            username='admin_a',
            defaults={
                'email': 'admin@tenant-a.com',
                'first_name': 'Administrador',
                'last_name': 'Tenant A',
                'role': 'admin',
                'tenant': tenant_a,
                'phone': '987654321',
                'address': 'Lima, Perú',
                'email_verified': True,
                'is_new_user': False,
            }
        )
        if created:
            admin_a.set_password('admin123')
            admin_a.save()
            self.stdout.write(f'✓ Admin Tenant A creado: {admin_a.username}')
        
        user_a, created = User.objects.get_or_create(
            username='user_a',
            defaults={
                'email': 'user@tenant-a.com',
                'first_name': 'Usuario',
                'last_name': 'Tenant A',
                'role': 'employee',
                'tenant': tenant_a,
                'phone': '987654323',
                'address': 'Lima, Perú',
                'email_verified': True,
                'is_new_user': False,
            }
        )
        if created:
            user_a.set_password('user123')
            user_a.save()
            self.stdout.write(f'✓ Usuario Tenant A creado: {user_a.username}')
        
        # Crear usuarios para Tenant B
        admin_b, created = User.objects.get_or_create(
            username='admin_b',
            defaults={
                'email': 'admin@tenant-b.com',
                'first_name': 'Administrador',
                'last_name': 'Tenant B',
                'role': 'admin',
                'tenant': tenant_b,
                'phone': '987654324',
                'address': 'Cusco, Perú',
                'email_verified': True,
                'is_new_user': False,
            }
        )
        if created:
            admin_b.set_password('admin123')
            admin_b.save()
            self.stdout.write(f'✓ Admin Tenant B creado: {admin_b.username}')
        
        user_b, created = User.objects.get_or_create(
            username='user_b',
            defaults={
                'email': 'user@tenant-b.com',
                'first_name': 'Usuario',
                'last_name': 'Tenant B',
                'role': 'employee',
                'tenant': tenant_b,
                'phone': '987654325',
                'address': 'Cusco, Perú',
                'email_verified': True,
                'is_new_user': False,
            }
        )
        if created:
            user_b.set_password('user123')
            user_b.save()
            self.stdout.write(f'✓ Usuario Tenant B creado: {user_b.username}')
        
        # Crear perfiles de usuario
        for user in [admin_a, user_a, admin_b, user_b]:
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'language': 'es',
                    'theme': 'light',
                    'email_notifications': True,
                }
            )
            if created:
                self.stdout.write(f'✓ Perfil creado para: {user.username}')
        
        # Crear permisos por defecto para cada rol en cada tenant
        roles = ['admin', 'manager', 'employee', 'photographer', 'assistant']
        
        for tenant in [tenant_a, tenant_b]:
            for role in roles:
                permission, created = RolePermission.objects.get_or_create(
                    tenant=tenant,
                    role=role,
                    defaults=RolePermission.get_default_permissions(role)
                )
                if created:
                    self.stdout.write(f'✓ Permisos creados para {role} en {tenant.name}')
        
        # Crear configuraciones básicas para cada tenant
        configs = [
            ('general', 'company_logo', '', 'string', 'Logo de la empresa'),
            ('general', 'timezone', 'America/Lima', 'string', 'Zona horaria'),
            ('general', 'date_format', 'DD/MM/YYYY', 'string', 'Formato de fecha'),
            ('crm', 'auto_assign_leads', 'true', 'boolean', 'Asignar leads automáticamente'),
            ('commerce', 'tax_rate', '18', 'float', 'Tasa de impuesto (%)'),
        ]
        
        for tenant in [tenant_a, tenant_b]:
            for module, key, value, data_type, description in configs:
                config, created = TenantConfiguration.objects.get_or_create(
                    tenant=tenant,
                    module=module,
                    key=key,
                    defaults={
                        'value': value,
                        'data_type': data_type,
                        'description': description,
                    }
                )
                if created:
                    self.stdout.write(f'✓ Configuración {module}.{key} creada para {tenant.name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 ¡Configuración completada!\n\n'
                'Credenciales creadas:\n'
                '- Super Admin: superadmin / admin123\n'
                '- Admin Tenant A: admin_a / admin123\n'
                '- Usuario Tenant A: user_a / user123\n'
                '- Admin Tenant B: admin_b / admin123\n'
                '- Usuario Tenant B: user_b / user123\n'
            )
        )