from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.core.models import Tenant, User
from apps.crm.clientes.models import Cliente
from .models import Contract


class ContractsAPITests(APITestCase):
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
        self.base_url = '/api/crm/contracts/'

        self.cliente = Cliente.objects.create(
            tenant=self.tenant,
            nombre_completo='Juan Perez',
            tipo_cliente='particular',
            dni='12345678',
            telefono_contacto='987654321'
        )

    def test_create_contract_with_client(self):
        payload = {
            'title': 'Contrato Servicio Foto',
            'contract_type': 'PHOTO',
            'status': 'DRAFT',
            'amount': '120.50',
            'start_date': '2025-11-01',
            'client': self.cliente.id,
        }
        response = self.client.post(self.base_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contract.objects.filter(tenant=self.tenant).count(), 1)

    def test_list_contracts_filtered_by_tenant(self):
        Contract.objects.create(
            tenant=self.tenant,
            client=self.cliente,
            title='C1',
            contract_type='PHOTO',
            status='DRAFT',
            amount='100',
            start_date='2025-11-01',
        )
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_download_contract_pdf_not_implemented_without_weasyprint(self):
        contract = Contract.objects.create(
            tenant=self.tenant,
            client=self.cliente,
            title='C2',
            contract_type='PHOTO',
            status='DRAFT',
            amount='100',
            start_date='2025-11-01',
        )
        url = f"{self.base_url}{contract.id}/download/"
        response = self.client.get(url)
        # Si WeasyPrint no está instalado, esperamos 501
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_501_NOT_IMPLEMENTED])