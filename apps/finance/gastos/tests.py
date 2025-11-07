from decimal import Decimal
from django.urls import reverse 
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import User, Tenant

# --- CORRECCIÓN CLAVE ---
# Importaciones hacia el índice 'finance/models.py'
from ..models import (
    PersonalExpense, 
    ServiceExpense, 
    EstadosGastoPersonal, 
    EstadosGastoServicio
)

# ... (El resto del código de tests es el mismo) ...

class GastosBaseTestCase(APITestCase):
    """
    Clase base que configura 2 Tenants y 2 Usuarios
    para probar el aislamiento de datos de Gastos.
    """
    @classmethod
    def setUpTestData(cls):
        # --- CREAMOS 2 TENANTS ---
        cls.tenant_a = Tenant.objects.create(name="Estudio Fotográfico A", slug="tenant-a")
        cls.tenant_b = Tenant.objects.create(name="Estudio Fotográfico B", slug="tenant-b")
        # --- CREAMOS 2 USUARIOS ---
        cls.user_a = User.objects.create_user(
            username='user_a', 
            email='a@tenant.com', 
            password='password', 
            tenant=cls.tenant_a
        )
        cls.user_b = User.objects.create_user(
            username='user_b', 
            email='b@tenant.com', 
            password='password', 
            tenant=cls.tenant_b
        )
        # --- DATOS DE PRUEBA TENANT A ---
        cls.gasto_personal_a = PersonalExpense.objects.create(
            tenant=cls.tenant_a,
            created_by=cls.user_a,
            codigo='EMP001A',
            nombre='Empleado A1',
            cargo='Fotógrafo',
            salario_base=Decimal('1000.00'),
            bonificaciones=Decimal('100.00'),
            descuentos=Decimal('50.00'),
            estado=EstadosGastoPersonal.PENDIENTE
        )
        cls.gasto_servicio_a = ServiceExpense.objects.create(
            tenant=cls.tenant_a,
            created_by=cls.user_a,
            codigo='SRV001A',
            tipo='Luz',
            proveedor='Luz del Sur',
            monto=Decimal('150.50'),
            fecha_vencimiento='2025-11-10',
            periodo='Octubre 2025',
            estado=EstadosGastoServicio.PENDIENTE
        )
        cls.gasto_servicio_vencido_a = ServiceExpense.objects.create(
            tenant=cls.tenant_a,
            created_by=cls.user_a,
            codigo='SRV002A',
            tipo='Agua',
            proveedor='Sedapal',
            monto=Decimal('75.25'),
            fecha_vencimiento='2025-10-01',
            periodo='Septiembre 2025',
            estado=EstadosGastoServicio.VENCIDO
        )
        # --- DATOS DE PRUEBA TENANT B (Para probar aislamiento) ---
        cls.gasto_personal_b = PersonalExpense.objects.create(
            tenant=cls.tenant_b,
            created_by=cls.user_b,
            codigo='EMP999B',
            nombre='Empleado B (Secreto)',
            cargo='Otro',
            salario_base=Decimal('9999.00'),
            estado=EstadosGastoPersonal.PENDIENTE
        )

    def setUp(self):
        """ Autentica al usuario A y AÑADE EL HEADER DEL TENANT """
        self.client.force_authenticate(user=self.user_a)
        self.client.defaults['HTTP_X_TENANT_ID'] = self.tenant_a.id

# --- PRUEBAS PARA EL RESUMEN DE TARJETAS (GASTOS) ---
class FinancialSummaryViewTests(GastosBaseTestCase):
    
    def test_financial_summary_calculations(self):
        url = reverse('finance:financial-summary') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(Decimal(data['nomina_pendiente']), Decimal('1050.00'))
        self.assertEqual(Decimal(data['servicios_pendientes']), Decimal('150.50'))
        self.assertEqual(data['servicios_vencidos'], 1)

# --- PRUEBAS CRUD PARA GASTOS DE PERSONAL ---
class PersonalExpenseViewSetTests(GastosBaseTestCase):

    def test_list_personal_expenses(self):
        url = reverse('finance:personal-expense-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['nombre'], 'Empleado A1')

    def test_create_personal_expense(self):
        url = reverse('finance:personal-expense-list')
        data = {
            "codigo": "EMP003A", "nombre": "Nuevo Empleado", "cargo": "Diseñador",
            "salarioBase": "1500.00", "bonificaciones": "50.00", "descuentos": "0.00",
            "estado": "Pendiente"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PersonalExpense.objects.count(), 3) 
        nuevo_gasto = PersonalExpense.objects.get(codigo="EMP003A")
        self.assertEqual(nuevo_gasto.tenant, self.tenant_a)

    def test_tenant_isolation_retrieve(self):
        url = reverse(
            'finance:personal-expense-detail', 
            kwargs={'pk': self.gasto_personal_b.pk} 
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)