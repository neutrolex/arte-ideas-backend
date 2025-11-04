from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.core.models import Tenant, User
from .models import Cliente


class ClienteAPITests(APITestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name='Estudio A', slug='estudio-a', description='Demo',
            business_name='Estudio A', business_address='Dirección',
            business_phone='999999999', business_email='a@studio.com',
            business_ruc='12345678901'
        )
        self.user = User.objects.create_user(
            username='tester', password='pass1234', tenant=self.tenant
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.base_url = '/api/crm/clients/'

    def test_create_cliente_particular_requires_dni(self):
        payload = {
            'nombre_completo': 'Juan Perez',
            'tipo_cliente': 'particular',
            'telefono_contacto': '987654321',
            'email': 'juan@example.com',
            'direccion': 'Calle 123',
            'dni': '12345678'
        }
        response = self.client.post(self.base_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 1)

    def test_create_cliente_empresa_requires_ruc(self):
        payload = {
            'nombre_completo': 'Empresa XYZ',
            'tipo_cliente': 'empresa',
            'telefono_contacto': '987654322',
            'email': 'contacto@xyz.com',
            'direccion': 'Av. Principal',
            'ruc': '12345678901'
        }
        response = self.client.post(self.base_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 1)

    def test_list_clients_filtered_by_tenant(self):
        Cliente.objects.create(
            tenant=self.tenant,
            nombre_completo='Cliente A',
            tipo_cliente='particular',
            dni='12345678',
            telefono_contacto='999999999'
        )
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
