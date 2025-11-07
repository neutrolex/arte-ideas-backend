"""
Vistas del Commerce App - Arte Ideas
Vistas REST para gestión de pedidos
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Q, F, Count
from django.utils import timezone
from datetime import datetime, timedelta

from apps.commerce.permissions import CommercePermission, ProductPermission, OrderItemPermission
from apps.crm.models import Client
from .models import Order, OrderItem, Product
from .serializers import (
    OrderSerializer, OrderItemSerializer, OrderSummarySerializer,
    ClientAutocompleteSerializer, ProductSerializer
)
from .filters import OrderFilter


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de pedidos
    
    Proporciona operaciones CRUD completas para pedidos con:
    - Filtrado avanzado
    - Búsqueda por texto
    - Resumen de totales
    - Autocompletado de clientes
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, CommercePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OrderFilter
    search_fields = [
        'order_number', 'client__first_name', 'client__last_name',
        'client__email', 'client__phone', 'client__dni'
    ]
    ordering_fields = [
        'order_number', 'start_date', 'delivery_date', 'total',
        'status', 'client__first_name', 'client__last_name'
    ]
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Obtener pedidos del tenant actual"""
        user = self.request.user
        return Order.objects.filter(tenant=user.tenant).select_related('client', 'contract').prefetch_related('items')
    
    def get_permissions(self):
        """Configurar permisos según acción"""
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, CommercePermission]
        elif self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, CommercePermission]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated, CommercePermission]
        elif self.action in ['summary', 'autocomplete_clients']:
            self.permission_classes = [IsAuthenticated, CommercePermission]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """Crear pedido con tenant actual"""
        user = self.request.user
        serializer.save(tenant=user.tenant)
    
    def perform_update(self, serializer):
        """Actualizar pedido con tenant actual"""
        user = self.request.user
        serializer.save(tenant=user.tenant)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Obtener resumen de pedidos
        
        Retorna:
        - Total de pedidos
        - Monto total
        - Total pagado
        - Saldo total
        - Contadores por estado
        - Contadores por tipo de documento
        """
        queryset = self.get_queryset()
        
        # Calcular totales generales
        totals = queryset.aggregate(
            total_orders=Count('id'),
            total_amount=Sum('total'),
            total_paid=Sum('paid_amount'),
            total_balance=Sum('balance')
        )
        
        # Contar por estado
        status_counts = queryset.values('status').annotate(count=Count('id'))
        status_dict = {item['status']: item['count'] for item in status_counts}
        
        # Contar por tipo de documento
        doc_type_counts = queryset.values('document_type').annotate(count=Count('id'))
        doc_type_dict = {item['document_type']: item['count'] for item in doc_type_counts}
        
        # Identificar pedidos atrasados
        today = timezone.now().date()
        delayed_count = queryset.filter(
            delivery_date__lt=today,
            status__in=['pending', 'in_process']
        ).count()
        
        summary_data = {
            'total_orders': totals['total_orders'] or 0,
            'total_amount': totals['total_amount'] or 0,
            'total_paid': totals['total_paid'] or 0,
            'total_balance': totals['total_balance'] or 0,
            'pending_orders': status_dict.get('pending', 0),
            'in_process_orders': status_dict.get('in_process', 0),
            'completed_orders': status_dict.get('completed', 0),
            'delayed_orders': delayed_count,
            'cancelled_orders': status_dict.get('cancelled', 0),
            'proforma_orders': doc_type_dict.get('proforma', 0),
            'sale_note_orders': doc_type_dict.get('nota_venta', 0),
            'contract_orders': doc_type_dict.get('contrato', 0),
        }
        
        serializer = OrderSummarySerializer(summary_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def totals_summary(self, request):
        """
        Obtener resumen de totales absolutos
        
        Retorna:
        - total_absoluto: Suma total de todos los pedidos
        - saldo_absoluto: Suma total de saldos pendientes
        """
        queryset = self.get_queryset()
        
        # Calcular totales absolutos
        totals = queryset.aggregate(
            total_absoluto=Sum('total'),
            saldo_absoluto=Sum('balance')
        )
        
        return Response({
            'total_absoluto': totals['total_absoluto'] or 0,
            'saldo_absoluto': totals['saldo_absoluto'] or 0
        })
    
    @action(detail=False, methods=['get'])
    def autocomplete_clients(self, request):
        """
        Autocompletado de clientes
        
        Parámetros:
        - q: texto de búsqueda (nombre, email, teléfono, DNI)
        - client_type: filtrar por tipo de cliente (opcional)
        """
        query = request.query_params.get('q', '').strip()
        client_type = request.query_params.get('client_type', None)
        
        if not query or len(query) < 2:
            return Response({'results': []})
        
        # Buscar clientes del tenant actual
        clients = Client.objects.filter(tenant=request.user.tenant)
        
        # Aplicar filtros de búsqueda
        search_filter = (
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(dni__icontains=query) |
            Q(company_name__icontains=query)
        )
        
        clients = clients.filter(search_filter)
        
        # Filtrar por tipo de cliente si se especifica
        if client_type:
            clients = clients.filter(client_type=client_type)
        
        # Limitar resultados
        clients = clients[:10]
        
        serializer = ClientAutocompleteSerializer(clients, many=True)
        return Response({'results': serializer.data})
    
    @action(detail=True, methods=['post'])
    def mark_as_completed(self, request, pk=None):
        """Marcar pedido como completado"""
        order = self.get_object()
        
        if order.status == 'completed':
            return Response(
                {'detail': 'El pedido ya está completado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'completed'
        order.save()
        
        return Response({'detail': 'Pedido marcado como completado'})
    
    @action(detail=True, methods=['post'])
    def mark_as_cancelled(self, request, pk=None):
        """Marcar pedido como cancelado"""
        order = self.get_object()
        
        if order.status == 'cancelled':
            return Response(
                {'detail': 'El pedido ya está cancelado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if order.status == 'completed':
            return Response(
                {'detail': 'No se puede cancelar un pedido completado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        return Response({'detail': 'Pedido marcado como cancelado'})
    
    @action(detail=False, methods=['get'])
    def overdue_orders(self, request):
        """Obtener pedidos atrasados"""
        today = timezone.now().date()
        
        overdue_orders = self.get_queryset().filter(
            delivery_date__lt=today,
            status__in=['pending', 'in_process']
        ).order_by('delivery_date')
        
        page = self.paginate_queryset(overdue_orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(overdue_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Obtener pedidos por estado"""
        status_filter = request.query_params.get('status', None)
        
        if status_filter:
            queryset = self.get_queryset().filter(status=status_filter)
        else:
            # Agrupar por estado
            status_counts = self.get_queryset().values('status').annotate(
                count=Count('id'),
                total=Sum('total')
            ).order_by('status')
            
            return Response({'status_summary': list(status_counts)})
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming_deliveries(self, request):
        """Obtener próximas entregas"""
        today = timezone.now().date()
        next_week = today + timedelta(days=7)
        
        upcoming_orders = self.get_queryset().filter(
            delivery_date__range=[today, next_week],
            status__in=['pending', 'in_process']
        ).order_by('delivery_date')
        
        page = self.paginate_queryset(upcoming_orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(upcoming_orders, many=True)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de items de pedido"""
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, OrderItemPermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Obtener items del tenant actual"""
        user = self.request.user
        return OrderItem.objects.filter(order__tenant=user.tenant)
    
    def get_permissions(self):
        """Configurar permisos según acción"""
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, OrderItemPermission]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, OrderItemPermission]
        return super().get_permissions()


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de productos/servicios
    
    Maneja el catálogo de productos y servicios disponibles
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ProductPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'product_type']
    ordering_fields = ['name', 'unit_price', 'stock_quantity', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Obtener productos del tenant actual"""
        user = self.request.user
        return Product.objects.filter(tenant=user.tenant)
    
    def get_permissions(self):
        """Configurar permisos según acción"""
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, ProductPermission]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, ProductPermission]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """Crear producto con tenant actual"""
        user = self.request.user
        serializer.save(tenant=user.tenant)
    
    def perform_update(self, serializer):
        """Actualizar producto con tenant actual"""
        user = self.request.user
        serializer.save(tenant=user.tenant)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Obtener productos con bajo stock"""
        queryset = self.get_queryset().filter(
            stock_quantity__lte=F('min_stock'),
            is_active=True
        ).order_by('stock_quantity')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active_products(self, request):
        """Obtener productos activos"""
        queryset = self.get_queryset().filter(is_active=True)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Actualizar stock de producto"""
        product = self.get_object()
        quantity = request.data.get('quantity', 0)
        operation = request.data.get('operation', 'add')  # add o subtract
        
        try:
            quantity = int(quantity)
            if operation == 'subtract':
                quantity = -quantity
            
            product.stock_quantity += quantity
            product.save()
            
            return Response({'detail': f'Stock actualizado. Nuevo stock: {product.stock_quantity}'})
        
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Cantidad inválida'},
                status=status.HTTP_400_BAD_REQUEST
            )