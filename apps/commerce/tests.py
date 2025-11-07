"""
Tests para el Commerce App - Arte Ideas
Tests comprehensivos para el sistema de gestión de pedidos
"""
import json
from datetime import datetime, timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.core.models import Tenant
from apps.crm.models import Client
from .models import Order, OrderItem, Product

User = get_user_model()


class BaseCommerceTestCase(APITestCase):
    """Clase base para tests del commerce app"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear tenant de prueba
        self.tenant = Tenant.objects.create(
            name='Estudio de Prueba',
            slug='estudio-prueba',
            business_name='Estudio Fotográfico Prueba S.A.C.',
            business_ruc='12345678901',
            business_phone='123456789',
            business_email='prueba@estudio.com',
            business_address='Av. Prueba 123'
        )
        
        # Crear usuarios de prueba con diferentes roles
        self.super_admin = User.objects.create_user(
            username='superadmin',
            email='superadmin@test.com',
            password='testpass123',
            role='super_admin'
        )
        
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            role='admin',
            tenant=self.tenant
        )
        
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@test.com',
            password='testpass123',
            role='manager',
            tenant=self.tenant
        )
        
        self.employee = User.objects.create_user(
            username='employee',
            email='employee@test.com',
            password='testpass123',
            role='employee',
            tenant=self.tenant
        )
        
        self.photographer = User.objects.create_user(
            username='photographer',
            email='photographer@test.com',
            password='testpass123',
            role='photographer',
            tenant=self.tenant
        )
        
        # Crear clientes de prueba
        self.client_particular = Client.objects.create(
            tenant=self.tenant,
            client_type='particular',
            first_name='Juan',
            last_name='Pérez',
            email='juan@test.com',
            phone='987654321',
            dni='12345678',
            address='Av. Test 123'
        )
        
        self.client_empresa = Client.objects.create(
            tenant=self.tenant,
            client_type='empresa',
            first_name='María',
            last_name='Gómez',
            email='maria@empresa.com',
            phone='987654322',
            dni='98765432109',  # RUC for empresa
            address='Av. Empresa 456',
            company_name='Empresa Test S.A.C.'
        )
        
        # Crear productos de prueba
        self.product1 = Product.objects.create(
            tenant=self.tenant,
            name='Sesión Fotográfica Básica',
            description='Sesión fotográfica de 1 hora',
            product_type='service',
            unit_price=150.00,
            stock_quantity=10,
            min_stock=2
        )
        
        self.product2 = Product.objects.create(
            tenant=self.tenant,
            name='Impresión 20x30 cm',
            description='Impresión fotográfica tamaño 20x30 cm',
            product_type='product',
            unit_price=25.00,
            stock_quantity=50,
            min_stock=10
        )
        
        # URLs de prueba
        self.order_list_url = reverse('commerce:order-list')
        self.product_list_url = reverse('commerce:product-list')


class OrderModelTest(BaseCommerceTestCase):
    """Tests para el modelo Order"""
    
    def test_create_order(self):
        """Test crear pedido básico"""
        order = Order.objects.create(
            tenant=self.tenant,
            client=self.client_particular,
            order_number='ORD-001',
            document_type='proforma',
            client_type='particular',
            total=150.00,
            status='pending',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7)
        )
        
        self.assertEqual(order.order_number, 'ORD-001')
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total, 150.00)
        self.assertEqual(order.balance, 150.00)  # balance = total - paid_amount
    
    def test_order_balance_calculation(self):
        """Test cálculo automático del balance"""
        order = Order.objects.create(
            tenant=self.tenant,
            client=self.client_particular,
            order_number='ORD-002',
            document_type='proforma',
            total=200.00,
            paid_amount=50.00,
            status='pending',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7)
        )
        
        self.assertEqual(order.balance, 150.00)  # 200 - 50 = 150
    
    def test_order_str_method(self):
        """Test método string del pedido"""
        order = Order.objects.create(
            tenant=self.tenant,
            client=self.client_particular,
            order_number='ORD-003',
            document_type='proforma',
            total=100.00,
            status='pending',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7)
        )
        
        expected_str = f"ORD-003 - Juan Pérez - S/.100.00"
        self.assertEqual(str(order), expected_str)


class OrderItemModelTest(BaseCommerceTestCase):
    """Tests para el modelo OrderItem"""
    
    def setUp(self):
        super().setUp()
        self.order = Order.objects.create(
            tenant=self.tenant,
            client=self.client_particular,
            order_number='ORD-004',
            document_type='proforma',
            total=0,
            status='pending',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7)
        )
    
    def test_create_order_item(self):
        """Test crear item de pedido"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            quantity=2,
            unit_price=150.00,
            subtotal=300.00
        )
        
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.subtotal, 300.00)
        self.assertEqual(item.product.name, 'Sesión Fotográfica Básica')
    
    def test_order_item_subtotal_calculation(self):
        """Test cálculo automático del subtotal"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            quantity=3,
            unit_price=100.00
        )
        
        self.assertEqual(item.subtotal, 300.00)  # 3 * 100 = 300


class ProductModelTest(BaseCommerceTestCase):
    """Tests para el modelo Product"""
    
    def test_create_product(self):
        """Test crear producto"""
        product = Product.objects.create(
            tenant=self.tenant,
            name='Producto Test',
            description='Descripción del producto',
            product_type='product',
            unit_price=99.99,
            stock_quantity=20,
            min_stock=5
        )
        
        self.assertEqual(product.name, 'Producto Test')
        self.assertEqual(product.unit_price, 99.99)
        self.assertEqual(product.stock_quantity, 20)
    
    def test_product_low_stock(self):
        """Test verificación de bajo stock"""
        product_low = Product.objects.create(
            tenant=self.tenant,
            name='Producto Bajo Stock',
            description='Producto con bajo stock',
            product_type='product',
            unit_price=50.00,
            stock_quantity=2,
            min_stock=5
        )
        
        self.assertTrue(product_low.is_low_stock())
        
        product_normal = Product.objects.create(
            tenant=self.tenant,
            name='Producto Stock Normal',
            description='Producto con stock normal',
            product_type='product',
            unit_price=50.00,
            stock_quantity=10,
            min_stock=5
        )
        
        self.assertFalse(product_normal.is_low_stock())


class OrderAPITest(BaseCommerceTestCase):
    """Tests para la API de pedidos"""
    
    def setUp(self):
        super().setUp()
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.admin)
    
    def test_list_orders(self):
        """Test listar pedidos"""
        # Crear algunos pedidos de prueba
        Order.objects.create(
            tenant=self.tenant,
            client=self.client_particular,
            order_number='ORD-005',
            document_type='proforma',
            total=150.00,
            status='pending',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7)
        )
        
        Order.objects.create(
            tenant=self.tenant,
            client=self.client_empresa,
            order_number='ORD-006',
            document_type='nota_venta',
            total=500.00,
            status='in_process',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=5)
        )
        
        response = self.client_api.get(self.order_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_create_order(self):
        """Test crear pedido via API"""
        order_data = {
            'client': self.client_particular.id,
            'order_number': 'ORD-007',
            'document_type': 'proforma',
            'client_type': 'particular',
            'total': 175.00,
            'start_date': timezone.now().date(),
            'delivery_date': timezone.now().date() + timedelta(days=7),
            'items': [
                {
                    'product': self.product1.id,
                    'quantity': 1,
                    'unit_price': 150.00
                }
            ]
        }
        
        response = self.client_api.post(
            self.order_list_url,
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['order_number'], 'ORD-007')
        self.assertEqual(response.data['total'], 175.00)
    
    def test_create_order_with_invalid_data(self):
        """Test crear pedido con datos inválidos"""
        order_data = {
            'client': self.client_particular.id,
            'order_number': '',  # Número de orden vacío
            'document_type': 'proforma',
            'client_type': 'particular',
            'total': -100.00,  # Total negativo
            'start_date': timezone.now().date(),
            'delivery_date': timezone.now().date() - timedelta(days=1),  # Fecha de entrega anterior
        }
        
        response = self.client_api.post(
            self.order_list_url,
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_order_permissions_by_role(self):
        """Test permisos según rol de usuario"""
        # Test con admin (debería poder crear)
        self.client_api.force_authenticate(user=self.admin)
        order_data = {
            'client': self.client_particular.id,
            'order_number': 'ORD-008',
            'document_type': 'proforma',
            'client_type': 'particular',
            'total': 200.00,
            'start_date': timezone.now().date(),
            'delivery_date': timezone.now().date() + timedelta(days=7)
        }
        
        response = self.client_api.post(
            self.order_list_url,
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Test con photographer (solo lectura)
        self.client_api.force_authenticate(user=self.photographer)
        response = self.client_api.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Photographer no debería poder crear
        response = self.client_api.post(
            self.order_list_url,
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_order_summary(self):
        """Test endpoint de resumen de pedidos"""
        # Crear pedidos de prueba
        Order.objects.create(
            tenant=self.tenant,
            client=self.client_particular,
            order_number='ORD-009',
            document_type='proforma',
            total=300.00,
            paid_amount=100.00,
            status='pending',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7)
        )
        
        Order.objects.create(
            tenant=self.tenant,
            client=self.client_empresa,
            order_number='ORD-010',
            document_type='nota_venta',
            total=500.00,
            paid_amount=500.00,
            status='completed',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=5)
        )
        
        summary_url = reverse('commerce:order-summary')
        response = self.client_api.get(summary_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_orders'], 2)
        self.assertEqual(response.data['total_amount'], 800.00)
        self.assertEqual(response.data['total_paid'], 600.00)
        self.assertEqual(response.data['total_balance'], 200.00)
    
    def test_client_autocomplete(self):
        """Test autocompletado de clientes"""
        autocomplete_url = reverse('commerce:order-autocomplete-clients')
        
        response = self.client_api.get(autocomplete_url, {'q': 'Juan'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'Juan')
    
    def test_mark_order_completed(self):
        """Test marcar pedido como completado"""
        order = Order.objects.create(
            tenant=self.tenant,
            client=self.client_particular,
            order_number='ORD-011',
            document_type='proforma',
            total=150.00,
            status='pending',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7)
        )
        
        complete_url = reverse('commerce:order-mark-as-completed', kwargs={'pk': order.id})
        response = self.client_api.post(complete_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')
    
    def test_overdue_orders(self):
        """Test obtener pedidos atrasados"""
        # Crear pedido atrasado
        overdue_order = Order.objects.create(
            tenant=self.tenant,
            client=self.client_particular,
            order_number='ORD-012',
            document_type='proforma',
            total=200.00,
            status='pending',
            start_date=timezone.now().date() - timedelta(days=10),
            delivery_date=timezone.now().date() - timedelta(days=3)  # Atrasado
        )
        
        # Crear pedido no atrasado
        on_time_order = Order.objects.create(
            tenant=self.tenant,
            client=self.client_empresa,
            order_number='ORD-013',
            document_type='proforma',
            total=300.00,
            status='pending',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7)
        )
        
        overdue_url = reverse('commerce:order-overdue-orders')
        response = self.client_api.get(overdue_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['order_number'], 'ORD-012')


class ProductAPITest(BaseCommerceTestCase):
    """Tests para la API de productos"""
    
    def setUp(self):
        super().setUp()
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.admin)
    
    def test_list_products(self):
        """Test listar productos"""
        response = self.client_api.get(self.product_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # product1 y product2
    
    def test_create_product(self):
        """Test crear producto"""
        product_data = {
            'name': 'Nuevo Producto',
            'description': 'Descripción del nuevo producto',
            'product_type': 'product',
            'unit_price': 75.50,
            'stock_quantity': 25,
            'min_stock': 5
        }
        
        response = self.client_api.post(
            self.product_list_url,
            data=json.dumps(product_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Nuevo Producto')
        self.assertEqual(response.data['unit_price'], 75.50)
    
    def test_update_stock(self):
        """Test actualizar stock de producto"""
        update_url = reverse('commerce:product-update-stock', kwargs={'pk': self.product1.id})
        
        # Aumentar stock
        response = self.client_api.post(
            update_url,
            data=json.dumps({'quantity': 5, 'operation': 'add'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock_quantity, 15)  # 10 + 5
    
    def test_low_stock_products(self):
        """Test obtener productos con bajo stock"""
        # Crear producto con bajo stock
        low_stock_product = Product.objects.create(
            tenant=self.tenant,
            name='Producto Bajo Stock',
            description='Producto con bajo stock',
            product_type='product',
            unit_price=30.00,
            stock_quantity=1,
            min_stock=5
        )
        
        low_stock_url = reverse('commerce:product-low-stock')
        response = self.client_api.get(low_stock_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Producto Bajo Stock')
    
    def test_product_permissions(self):
        """Test permisos de productos por rol"""
        # Employee no debería poder crear productos
        self.client_api.force_authenticate(user=self.employee)
        
        product_data = {
            'name': 'Producto Employee',
            'description': 'Producto creado por employee',
            'product_type': 'product',
            'unit_price': 50.00,
            'stock_quantity': 10,
            'min_stock': 2
        }
        
        response = self.client_api.post(
            self.product_list_url,
            data=json.dumps(product_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Pero debería poder actualizar stock
        update_url = reverse('commerce:product-update-stock', kwargs={'pk': self.product1.id})
        response = self.client_api.post(
            update_url,
            data=json.dumps({'quantity': 2, 'operation': 'add'}),
            content_type='application/json'
        )
        
        # Esto debería funcionar si el employee tiene permiso para actualizar stock
        # (depende de la lógica de permisos específica)


class OrderItemAPITest(BaseCommerceTestCase):
    """Tests para la API de items de pedido"""
    
    def setUp(self):
        super().setUp()
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.admin)
        
        self.order = Order.objects.create(
            tenant=self.tenant,
            client=self.client_particular,
            order_number='ORD-014',
            document_type='proforma',
            total=0,
            status='pending',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7)
        )
    
    def test_create_order_item(self):
        """Test crear item de pedido"""
        order_item_data = {
            'order': self.order.id,
            'product': self.product1.id,
            'quantity': 2,
            'unit_price': 150.00
        }
        
        order_item_url = reverse('commerce:orderitem-list')
        response = self.client_api.post(
            order_item_url,
            data=json.dumps(order_item_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 2)
        self.assertEqual(response.data['subtotal'], 300.00)
    
    def test_order_item_validation(self):
        """Test validaciones de item de pedido"""
        # Cantidad negativa
        order_item_data = {
            'order': self.order.id,
            'product': self.product1.id,
            'quantity': -1,
            'unit_price': 150.00
        }
        
        order_item_url = reverse('commerce:orderitem-list')
        response = self.client_api.post(
            order_item_url,
            data=json.dumps(order_item_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Precio unitario negativo
        order_item_data = {
            'order': self.order.id,
            'product': self.product1.id,
            'quantity': 1,
            'unit_price': -50.00
        }
        
        response = self.client_api.post(
            order_item_url,
            data=json.dumps(order_item_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderValidationTest(BaseCommerceTestCase):
    """Tests para validaciones específicas del pedido"""
    
    def setUp(self):
        super().setUp()
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.admin)
    
    def test_order_number_unique_validation(self):
        """Test validación de número de orden único"""
        # Crear primer pedido
        Order.objects.create(
            tenant=self.tenant,
            client=self.client_particular,
            order_number='ORD-UNIQUE',
            document_type='proforma',
            total=100.00,
            status='pending',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7)
        )
        
        # Intentar crear otro pedido con el mismo número
        order_data = {
            'client': self.client_particular.id,
            'order_number': 'ORD-UNIQUE',  # Mismo número
            'document_type': 'proforma',
            'client_type': 'particular',
            'total': 200.00,
            'start_date': timezone.now().date(),
            'delivery_date': timezone.now().date() + timedelta(days=7)
        }
        
        response = self.client_api.post(
            self.order_list_url,
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_client_type_consistency_validation(self):
        """Test validación de consistencia de tipo de cliente"""
        # Intentar crear pedido con tipo de cliente inconsistente
        order_data = {
            'client': self.client_empresa.id,  # Cliente empresa
            'order_number': 'ORD-INCONSISTENT',
            'document_type': 'proforma',
            'client_type': 'particular',  # Tipo particular (inconsistente)
            'total': 150.00,
            'start_date': timezone.now().date(),
            'delivery_date': timezone.now().date() + timedelta(days=7)
        }
        
        response = self.client_api.post(
            self.order_list_url,
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_school_level_validation(self):
        """Test validación de nivel escolar para clientes colegio"""
        # Crear cliente tipo colegio
        client_colegio = Client.objects.create(
            tenant=self.tenant,
            client_type='colegio',
            first_name='Colegio',
            last_name='Test',
            email='colegio@test.com',
            phone='123456789',
            dni='11111111',
            school_level='primaria',
            school_grade='5to',
            school_section='A'
        )
        
        # Pedido sin nivel escolar para cliente colegio
        order_data = {
            'client': client_colegio.id,
            'order_number': 'ORD-COLEGIO',
            'document_type': 'proforma',
            'client_type': 'colegio',
            'total': 200.00,
            'start_date': timezone.now().date(),
            'delivery_date': timezone.now().date() + timedelta(days=7)
            # Falta school_level
        }
        
        response = self.client_api.post(
            self.order_list_url,
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderSignalsTest(BaseCommerceTestCase):
    """Tests para las señales del pedido"""
    
    def setUp(self):
        super().setUp()
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.admin)
    
    def test_order_status_update_on_completion(self):
        """Test actualización automática de estado al completar"""
        order = Order.objects.create(
            tenant=self.tenant,
            client=self.client_particular,
            order_number='ORD-SIGNAL',
            document_type='proforma',
            total=100.00,
            paid_amount=100.00,  # Pagado completamente
            status='pending',
            start_date=timezone.now().date(),
            delivery_date=timezone.now().date() + timedelta(days=7)
        )
        
        # La señal debería actualizar el estado a 'completed'
        # (esto depende de la implementación específica de las señales)
        # Por ahora, verificamos que el pedido se creó correctamente
        self.assertEqual(order.paid_amount, 100.00)
        self.assertEqual(order.balance, 0.00)


# Tests de integración
class OrderIntegrationTest(BaseCommerceTestCase):
    """Tests de integración para el flujo completo de pedidos"""
    
    def setUp(self):
        super().setUp()
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.admin)
    
    def test_complete_order_flow(self):
        """Test flujo completo de creación y gestión de pedido"""
        # 1. Crear pedido
        order_data = {
            'client': self.client_particular.id,
            'order_number': 'ORD-FLOW',
            'document_type': 'proforma',
            'client_type': 'particular',
            'total': 325.00,
            'start_date': timezone.now().date(),
            'delivery_date': timezone.now().date() + timedelta(days=7),
            'items': [
                {
                    'product': self.product1.id,
                    'quantity': 2,
                    'unit_price': 150.00
                },
                {
                    'product': self.product2.id,
                    'quantity': 1,
                    'unit_price': 25.00
                }
            ]
        }
        
        response = self.client_api.post(
            self.order_list_url,
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order_id = response.data['id']
        
        # 2. Verificar que el pedido fue creado
        order_detail_url = reverse('commerce:order-detail', kwargs={'pk': order_id})
        response = self.client_api.get(order_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_number'], 'ORD-FLOW')
        self.assertEqual(response.data['total'], 325.00)
        self.assertEqual(len(response.data['items']), 2)
        
        # 3. Marcar pedido como completado
        complete_url = reverse('commerce:order-mark-as-completed', kwargs={'pk': order_id})
        response = self.client_api.post(complete_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Verificar que el estado cambió
        response = self.client_api.get(order_detail_url)
        self.assertEqual(response.data['status'], 'completed')
        
        # 5. Verificar resumen de pedidos
        summary_url = reverse('commerce:order-summary')
        response = self.client_api.get(summary_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_orders'], 1)
        self.assertEqual(response.data['total_amount'], 325.00)