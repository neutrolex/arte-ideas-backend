"""
Tests para el endpoint totals_summary de pedidos
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from apps.core.models import Tenant
from apps.crm.models import Client
from apps.commerce.models import Order


User = get_user_model()


class OrderTotalsSummaryTestCase(TestCase):
    """Test case para el endpoint totals_summary"""
    
    def setUp(self):
        """Configuración inicial del test"""
        # Crear tenant
        self.tenant = Tenant.objects.create(
            name="Test Tenant",
            slug="test",
            business_name="Test Business",
            business_address="Test Address",
            business_phone="123456789",
            business_email="test@example.com",
            business_ruc="12345678901"
        )
        
        # Crear usuario administrador
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            tenant=self.tenant,
            role="admin"
        )
        
        # Crear cliente
        self.client_obj = Client.objects.create(
            tenant=self.tenant,
            first_name="Juan",
            last_name="Pérez",
            email="juan@test.com",
            phone="123456789",
            dni="12345678",
            address="Test Address",
            client_type="particular"
        )
        
        # Crear pedidos de prueba
        self.order1 = Order.objects.create(
            tenant=self.tenant,
            order_number="ORD-001",
            client=self.client_obj,
            document_type="proforma",
            client_type="particular",
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7),
            total=1000.00,
            paid_amount=500.00,
            balance=500.00,
            status="pending"
        )
        
        self.order2 = Order.objects.create(
            tenant=self.tenant,
            order_number="ORD-002",
            client=self.client_obj,
            document_type="nota_venta",
            client_type="particular",
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=14),
            total=2000.00,
            paid_amount=1500.00,
            balance=500.00,
            status="in_process"
        )
        
        self.order3 = Order.objects.create(
            tenant=self.tenant,
            order_number="ORD-003",
            client=self.client_obj,
            document_type="contrato",
            client_type="colegio",
            school_level="primaria",
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=21),
            total=3000.00,
            paid_amount=3000.00,
            balance=0.00,
            status="completed"
        )
        
        # Configurar cliente API
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
    
    def test_totals_summary_success(self):
        """Test que el endpoint totals_summary retorna los valores correctos"""
        response = self.client.get('/api/commerce/orders/totals_summary/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        
        # Verificar estructura de respuesta
        self.assertIn('total_absoluto', data)
        self.assertIn('saldo_absoluto', data)
        
        # Verificar cálculos
        expected_total = 6000.00  # 1000 + 2000 + 3000
        expected_balance = 1000.00  # 500 + 500 + 0
        
        self.assertEqual(float(data['total_absoluto']), expected_total)
        self.assertEqual(float(data['saldo_absoluto']), expected_balance)
    
    def test_totals_summary_empty_orders(self):
        """Test que el endpoint funciona cuando no hay pedidos"""
        # Eliminar todos los pedidos
        Order.objects.all().delete()
        
        response = self.client.get('/api/commerce/orders/totals_summary/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        
        # Verificar que retorne 0 cuando no hay pedidos
        self.assertEqual(float(data['total_absoluto']), 0.00)
        self.assertEqual(float(data['saldo_absoluto']), 0.00)
    
    def test_totals_summary_with_negative_values(self):
        """Test que el endpoint maneja valores negativos correctamente"""
        # Crear pedido con valores negativos (no debería pasar en producción)
        order4 = Order.objects.create(
            tenant=self.tenant,
            order_number="ORD-004",
            client=self.client_obj,
            document_type="proforma",
            client_type="particular",
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=28),
            total=-500.00,  # Valor negativo
            paid_amount=0.00,
            balance=-500.00,  # Valor negativo
            status="cancelled"
        )
        
        response = self.client.get('/api/commerce/orders/totals_summary/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        
        # Verificar que sume correctamente incluso con valores negativos
        expected_total = 5500.00  # 1000 + 2000 + 3000 - 500
        expected_balance = 500.00  # 500 + 500 + 0 - 500
        
        self.assertEqual(float(data['total_absoluto']), expected_total)
        self.assertEqual(float(data['saldo_absoluto']), expected_balance)
    
    def test_totals_summary_requires_authentication(self):
        """Test que el endpoint requiere autenticación"""
        # Desautenticar el cliente
        self.client.force_authenticate(user=None)
        
        response = self.client.get('/api/commerce/orders/totals_summary/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_totals_summary_respects_tenant_isolation(self):
        """Test que el endpoint solo retorna pedidos del tenant actual"""
        # Crear otro tenant y pedido
        other_tenant = Tenant.objects.create(
            name="Other Tenant",
            slug="other",
            business_name="Other Business",
            business_address="Other Address",
            business_phone="987654321",
            business_email="other@example.com",
            business_ruc="98765432109"
        )
        
        other_user = User.objects.create_user(
            username="other_admin",
            email="other@test.com",
            password="testpass123",
            tenant=other_tenant,
            role="admin"
        )
        
        other_client = Client.objects.create(
            tenant=other_tenant,
            first_name="Otro",
            last_name="Cliente",
            email="otro@test.com",
            phone="987654321",
            dni="87654321",
            address="Other Address",
            client_type="particular"
        )
        
        # Crear pedido en otro tenant
        Order.objects.create(
            tenant=other_tenant,
            order_number="ORD-OTHER",
            client=other_client,
            document_type="proforma",
            client_type="particular",
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7),
            total=9999.00,
            paid_amount=0.00,
            balance=9999.00,
            status="pending"
        )
        
        response = self.client.get('/api/commerce/orders/totals_summary/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        
        # Verificar que no incluye el pedido del otro tenant
        expected_total = 6000.00  # Solo los pedidos del tenant actual
        expected_balance = 1000.00
        
        self.assertEqual(float(data['total_absoluto']), expected_total)
        self.assertEqual(float(data['saldo_absoluto']), expected_balance)
    
    def test_totals_summary_endpoint_url(self):
        """Test que el endpoint está disponible en la URL correcta"""
        # Verificar que la URL existe y responde
        response = self.client.get('/api/commerce/orders/totals_summary/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el endpoint está registrado
        from django.urls import reverse, resolve
        
        # La URL debería ser accesible
        try:
            resolve('/api/commerce/orders/totals_summary/')
            url_exists = True
        except:
            url_exists = False
        
        self.assertTrue(url_exists, "El endpoint totals_summary no está correctamente registrado")
    
    def test_totals_summary_response_format(self):
        """Test que el formato de respuesta es el esperado"""
        response = self.client.get('/api/commerce/orders/totals_summary/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar content-type
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = response.json()
        
        # Verificar que los valores sean números decimales
        self.assertIsInstance(data['total_absoluto'], (int, float))
        self.assertIsInstance(data['saldo_absoluto'], (int, float))
        
        # Verificar que no haya campos adicionales no esperados
        expected_fields = {'total_absoluto', 'saldo_absoluto'}
        actual_fields = set(data.keys())
        
        self.assertEqual(actual_fields, expected_fields)
    
    def test_totals_summary_method_not_allowed(self):
        """Test que solo se permite método GET"""
        # Probar POST
        response = self.client.post('/api/commerce/orders/totals_summary/', {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Probar PUT
        response = self.client.put('/api/commerce/orders/totals_summary/', {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Probar DELETE
        response = self.client.delete('/api/commerce/orders/totals_summary/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)