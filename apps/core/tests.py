"""
Tests del Core App - Arte Ideas
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Tenant, UserProfile, RolePermission

User = get_user_model()


class TenantModelTest(TestCase):
    """Tests para el modelo Tenant"""
    
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Test Studio",
            business_name="Test Business",
            business_address="Test Address",
            business_phone="123456789",
            business_email="test@test.com",
            business_ruc="12345678901",
            location_type="lima"
        )
    
    def test_tenant_creation(self):
        """Test creación de tenant"""
        self.assertEqual(self.tenant.name, "Test Studio")
        self.assertTrue(self.tenant.has_global_data_access())
        self.assertTrue(self.tenant.has_financial_modules())
    
    def test_tenant_slug_generation(self):
        """Test generación automática de slug"""
        self.assertIsNotNone(self.tenant.slug)


class UserModelTest(TestCase):
    """Tests para el modelo User"""
    
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Test Studio",
            business_name="Test Business",
            business_address="Test Address",
            business_phone="123456789",
            business_email="test@test.com",
            business_ruc="12345678901"
        )
        
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass123",
            tenant=self.tenant,
            role="employee"
        )
    
    def test_user_creation(self):
        """Test creación de usuario"""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.tenant, self.tenant)
        self.assertEqual(self.user.role, "employee")
    
    def test_user_permissions(self):
        """Test sistema de permisos"""
        permissions = self.user.get_permissions_list()
        self.assertIn('access:dashboard', permissions)
        self.assertTrue(self.user.has_permission('access:dashboard'))


class AuthenticationAPITest(APITestCase):
    """Tests para autenticación JWT"""
    
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Test Studio",
            business_name="Test Business",
            business_address="Test Address",
            business_phone="123456789",
            business_email="test@test.com",
            business_ruc="12345678901"
        )
        
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass123",
            tenant=self.tenant,
            role="admin"
        )
        
        # Crear perfil
        UserProfile.objects.create(user=self.user)
    
    def test_login(self):
        """Test login JWT"""
        url = reverse('core:token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_profile_access(self):
        """Test acceso al perfil"""
        # Obtener token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = reverse('core:profile:profile_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class ProfileAPITest(APITestCase):
    """Tests para APIs de perfil"""
    
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Test Studio",
            business_name="Test Business",
            business_address="Test Address",
            business_phone="123456789",
            business_email="test@test.com",
            business_ruc="12345678901"
        )
        
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass123",
            tenant=self.tenant,
            role="admin"
        )
        
        UserProfile.objects.create(user=self.user)
        
        # Autenticar
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def test_get_profile_statistics(self):
        """Test obtener estadísticas del perfil"""
        url = reverse('core:profile:statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('orders_processed', response.data)
        self.assertIn('clients_attended', response.data)
    
    def test_change_password(self):
        """Test cambio de contraseña"""
        url = reverse('core:profile:change_password')
        data = {
            'current_password': 'testpass123',
            'new_password': 'newpass123',
            'confirm_password': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ConfigurationAPITest(APITestCase):
    """Tests para APIs de configuración"""
    
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Test Studio",
            business_name="Test Business",
            business_address="Test Address",
            business_phone="123456789",
            business_email="test@test.com",
            business_ruc="12345678901"
        )
        
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="adminpass123",
            tenant=self.tenant,
            role="admin"
        )
        
        self.employee_user = User.objects.create_user(
            username="employee",
            email="employee@test.com",
            password="emppass123",
            tenant=self.tenant,
            role="employee"
        )
        
        UserProfile.objects.create(user=self.admin_user)
        UserProfile.objects.create(user=self.employee_user)
        
        # Crear permisos por defecto
        RolePermission.objects.create(
            tenant=self.tenant,
            role="admin",
            **RolePermission.get_default_permissions("admin")
        )
    
    def test_business_config_access_admin(self):
        """Test acceso a configuración del negocio como admin"""
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = reverse('core:configuration:business_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Studio')
    
    def test_business_config_access_employee(self):
        """Test acceso denegado a configuración como employee"""
        refresh = RefreshToken.for_user(self.employee_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = reverse('core:configuration:business_edit')
        response = self.client.put(url, {'business_name': 'New Name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_users_management(self):
        """Test gestión de usuarios"""
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = reverse('core:configuration:users_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Debe mostrar solo el employee (no el admin actual)
        self.assertEqual(len(response.data), 1)


class MultiTenancyTest(APITestCase):
    """Tests para aislamiento multi-tenant"""
    
    def setUp(self):
        # Tenant A
        self.tenant_a = Tenant.objects.create(
            name="Studio A",
            business_name="Business A",
            business_address="Address A",
            business_phone="111111111",
            business_email="a@test.com",
            business_ruc="11111111111"
        )
        
        # Tenant B
        self.tenant_b = Tenant.objects.create(
            name="Studio B",
            business_name="Business B",
            business_address="Address B",
            business_phone="222222222",
            business_email="b@test.com",
            business_ruc="22222222222"
        )
        
        # Usuario de Tenant A
        self.user_a = User.objects.create_user(
            username="user_a",
            email="user_a@test.com",
            password="pass123",
            tenant=self.tenant_a,
            role="admin"
        )
        
        # Usuario de Tenant B
        self.user_b = User.objects.create_user(
            username="user_b",
            email="user_b@test.com",
            password="pass123",
            tenant=self.tenant_b,
            role="admin"
        )
        
        UserProfile.objects.create(user=self.user_a)
        UserProfile.objects.create(user=self.user_b)
    
    def test_tenant_isolation(self):
        """Test aislamiento entre tenants"""
        # Usuario A no debe ver usuarios de Tenant B
        refresh = RefreshToken.for_user(self.user_a)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = reverse('core:configuration:users_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # No debe haber usuarios (solo ve usuarios de su tenant, excluyendo a sí mismo)
        self.assertEqual(len(response.data), 0)
    
    def test_business_config_isolation(self):
        """Test aislamiento de configuración de negocio"""
        refresh = RefreshToken.for_user(self.user_a)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = reverse('core:configuration:business_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Studio A')
        self.assertNotEqual(response.data['name'], 'Studio B')