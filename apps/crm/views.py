"""
Vistas del CRM App - Arte Ideas
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Cliente, Contrato
from .serializers import ClienteSerializer, ContratoSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de clientes
    """
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_cliente', 'activo']
    search_fields = ['nombres', 'apellidos', 'email', 'telefono', 'dni', 'razon_social']
    ordering_fields = ['nombres', 'apellidos', 'creado_en']
    ordering = ['apellidos', 'nombres']

    def get_queryset(self):
        """Filtrar clientes por tenant del usuario"""
        if self.request.user.is_superuser:
            return Cliente.objects.all()
        return Cliente.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        """Asignar tenant automáticamente al crear"""
        serializer.save(tenant=self.request.user.tenant)


class ContratoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de contratos
    """
    serializer_class = ContratoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'cliente']
    search_fields = ['numero_contrato', 'titulo', 'cliente__nombres', 'cliente__apellidos']
    ordering_fields = ['numero_contrato', 'fecha_inicio', 'creado_en']
    ordering = ['-creado_en']

    def get_queryset(self):
        """Filtrar contratos por tenant del usuario"""
        if self.request.user.is_superuser:
            return Contrato.objects.select_related('cliente').all()
        return Contrato.objects.select_related('cliente').filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        """Asignar tenant automáticamente al crear"""
        serializer.save(tenant=self.request.user.tenant)