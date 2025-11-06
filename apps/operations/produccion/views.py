from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import OrdenProduccion
from .serializers import OrdenProduccionSerializer
from .filters import OrdenProduccionFilter
from .permissions import IsSameInmobiliaria

class OrdenProduccionViewSet(viewsets.ModelViewSet):
    serializer_class = OrdenProduccionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = OrdenProduccionFilter
    search_fields = ['numero_op', 'cliente__first_name', 'cliente__last_name', 'pedido__order_number', 'descripcion']
    permission_classes = [IsSameInmobiliaria]
    
    def get_queryset(self):
        """Filtrar órdenes según el tipo de usuario"""
        user = self.request.user
        
        # Superusuarios ven todas las órdenes
        if user.is_superuser:
            return OrdenProduccion.objects.all().select_related('pedido', 'cliente', 'operario', 'id_inquilino')
        
        # Usuarios normales solo ven de su inquilino
        if hasattr(user, 'tenant') and user.tenant:
            return OrdenProduccion.objects.filter(
                id_inquilino=user.tenant
            ).select_related('pedido', 'cliente', 'operario')
        
        return OrdenProduccion.objects.none()
    
    def get_serializer_context(self):
        """Pasar contexto necesario al serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        
        if hasattr(self.request.user, 'tenant'):
            context['user_inquilino'] = self.request.user.tenant
        
        return context
    
    def perform_create(self, serializer):
        """Asignar automáticamente la inmobiliaria al crear"""
        # El serializer ya maneja la asignación automática
        serializer.save()
    
    def perform_update(self, serializer):
        """Prevenir cambios de inmobiliaria en actualizaciones"""
        # El serializer ya maneja la prevención de cambios
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Endpoint para obtener estadísticas por estado"""
        user = self.request.user
        
        # Superusuarios pueden ver estadísticas globales o por inquilino específico
        if user.is_superuser:
            # Si se pasa parámetro inquilino_id, filtrar por ese inquilino
            inquilino_id = request.query_params.get('inquilino_id')
            if inquilino_id:
                queryset = OrdenProduccion.objects.filter(id_inquilino_id=inquilino_id)
            else:
                queryset = OrdenProduccion.objects.all()
        else:
            # Usuarios normales solo ven estadísticas de su inquilino
            if hasattr(user, 'tenant') and user.tenant:
                queryset = OrdenProduccion.objects.filter(id_inquilino=user.tenant)
            else:
                return Response({'error': 'Usuario no asociado a un inquilino'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calcular estadísticas
        pendientes = queryset.filter(estado='Pendiente').count()
        en_proceso = queryset.filter(estado='En Proceso').count()
        terminados = queryset.filter(estado='Terminado').count()
        entregados = queryset.filter(estado='Entregado').count()
        total = queryset.count()
        
        return Response({
            'pendientes': pendientes,
            'en_proceso': en_proceso,
            'terminados': terminados,
            'entregados': entregados,
            'total': total
        })