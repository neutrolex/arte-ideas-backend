from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics, views
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, F, DecimalField, Count 
from django.db.models.functions import Coalesce
# Importaciones de CORE
from apps.core.viewsets import TenantViewSet
from apps.core.mixins import ExportMixin
from apps.core.permissions import TenantPermission

# --- CORRECCIÓN CLAVE ---
# Importaciones hacia el índice 'finance/models.py'
from ..models import (
    ExpenseCategory,
    PersonalExpense,
    ServiceExpense,
    Budget,
    EstadosGastoPersonal,
    EstadosGastoServicio
)
from ..serializers import (
    ExpenseCategorySerializer,
    PersonalExpenseSerializer,
    ServiceExpenseSerializer,
    BudgetSerializer,
)


class ExpenseCategoryViewSet(TenantViewSet):

    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'created_at']


class BudgetViewSet(TenantViewSet):

    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['categoria', 'periodo_inicio', 'periodo_fin']
    ordering_fields = ['periodo_inicio', 'monto_presupuestado']


class PersonalExpenseViewSet(TenantViewSet, ExportMixin):
    
    queryset = PersonalExpense.objects.all().order_by('-created_at')
    serializer_class = PersonalExpenseSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'cargo', 'categoria']
    search_fields = ['nombre', 'codigo']
    ordering_fields = ['nombre', 'salario_base', 'fecha_pago']

    export_formats = ['excel', 'csv'] 
    export_template_name = 'expenses_report_personal' 
    
    def get_export_filename(self):
        return 'reporte_gastos_personal'

    


class ServiceExpenseViewSet(TenantViewSet, ExportMixin):

    queryset = ServiceExpense.objects.all().order_by('-fecha_vencimiento')
    serializer_class = ServiceExpenseSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'tipo', 'proveedor', 'categoria']
    search_fields = ['proveedor', 'codigo', 'periodo']
    ordering_fields = ['fecha_vencimiento', 'monto', 'periodo']

    export_formats = ['excel', 'csv']
    export_template_name = 'expenses_report_service' 
    
    def get_export_filename(self):
        return 'reporte_gastos_servicios'

    

class FinancialSummaryView(views.APIView):
    """
    API endpoint (solo lectura)
    """
    permission_classes = [permissions.IsAuthenticated, TenantPermission]

    def get(self, request, *args, **kwargs):
        tenant = request.tenant

        # 1. Nómina Pendiente
        nomina_agregado = PersonalExpense.objects.filter(
            tenant=tenant,
            estado=EstadosGastoPersonal.PENDIENTE
        ).aggregate(
            total=Sum(
                F('salario_base') + F('bonificaciones') - F('descuentos'),
                output_field=DecimalField()
            )
        )
        
        # 2. Servicios Pendientes
        servicios_pend_agregado = ServiceExpense.objects.filter(
            tenant=tenant,
            estado=EstadosGastoServicio.PENDIENTE
        ).aggregate(
            total=Sum('monto')
        )

        # 3. Servicios Vencidos
        servicios_venc_conteo = ServiceExpense.objects.filter(
            tenant=tenant,
            estado=EstadosGastoServicio.VENCIDO
        ).aggregate(
            conteo=Count('id') 
        )

        
        data = {
            'nomina_pendiente': nomina_agregado['total'] or 0.00,
            'servicios_pendientes': servicios_pend_agregado['total'] or 0.00,
            'servicios_vencidos': servicios_venc_conteo['conteo'] or 0, 
        }
        return Response(data)