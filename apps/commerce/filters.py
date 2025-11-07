"""
Filtros del Commerce App - Arte Ideas
Filtros avanzados para búsqueda de pedidos
"""
import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
from datetime import datetime, timedelta

from .models import Order, OrderItem, Product


class OrderFilter(filters.FilterSet):
    """
    Filtros avanzados para el modelo Order
    
    Permite filtrar pedidos por múltiples criterios:
    - Cliente (nombre, apellido, email, teléfono, DNI)
    - Tipo de documento (proforma, nota_venta, contrato)
    - Estado del pedido (pendiente, en_proceso, completado, atrasado, cancelado)
    - Fechas (inicio, entrega, rango de fechas)
    - Tipo de cliente (particular, colegio, empresa)
    - Montos (total, pagado, saldo)
    - Contrato relacionado
    - Nivel escolar (para colegios)
    """
    
    # Filtros de texto para cliente
    client_name = filters.CharFilter(
        field_name='client__first_name',
        lookup_expr='icontains',
        label='Nombre del cliente'
    )
    
    client_last_name = filters.CharFilter(
        field_name='client__last_name',
        lookup_expr='icontains',
        label='Apellido del cliente'
    )
    
    client_email = filters.CharFilter(
        field_name='client__email',
        lookup_expr='icontains',
        label='Email del cliente'
    )
    
    client_phone = filters.CharFilter(
        field_name='client__phone',
        lookup_expr='icontains',
        label='Teléfono del cliente'
    )
    
    client_dni = filters.CharFilter(
        field_name='client__dni',
        lookup_expr='icontains',
        label='DNI del cliente'
    )
    
    # Filtro de búsqueda general (busca en múltiples campos)
    search = filters.CharFilter(
        method='filter_by_search',
        label='Búsqueda general'
    )
    
    # Filtros por tipo de documento
    document_type = filters.ChoiceFilter(
        field_name='document_type',
        choices=Order.DOCUMENT_TYPE_CHOICES,
        label='Tipo de documento'
    )
    
    # Filtros por estado
    status = filters.ChoiceFilter(
        field_name='status',
        choices=Order.ORDER_STATUS_CHOICES,
        label='Estado del pedido'
    )
    
    # Filtros por tipo de cliente
    client_type = filters.ChoiceFilter(
        field_name='client_type',
        choices=Order.CLIENT_TYPE_CHOICES,
        label='Tipo de cliente'
    )
    
    # Filtros por nivel escolar (para colegios)
    school_level = filters.ChoiceFilter(
        field_name='school_level',
        choices=Order.SCHOOL_LEVEL_CHOICES,
        label='Nivel escolar'
    )
    
    # Filtros por fechas
    start_date_from = filters.DateFilter(
        field_name='start_date',
        lookup_expr='gte',
        label='Fecha de inicio desde'
    )
    
    start_date_to = filters.DateFilter(
        field_name='start_date',
        lookup_expr='lte',
        label='Fecha de inicio hasta'
    )
    
    delivery_date_from = filters.DateFilter(
        field_name='delivery_date',
        lookup_expr='gte',
        label='Fecha de entrega desde'
    )
    
    delivery_date_to = filters.DateFilter(
        field_name='delivery_date',
        lookup_expr='lte',
        label='Fecha de entrega hasta'
    )
    
    # Filtros por rango de fechas
    date_range = filters.CharFilter(
        method='filter_by_date_range',
        label='Rango de fechas (YYYY-MM-DD,YYYY-MM-DD)'
    )
    
    # Filtros por montos
    total_min = filters.NumberFilter(
        field_name='total',
        lookup_expr='gte',
        label='Total mínimo'
    )
    
    total_max = filters.NumberFilter(
        field_name='total',
        lookup_expr='lte',
        label='Total máximo'
    )
    
    paid_amount_min = filters.NumberFilter(
        field_name='paid_amount',
        lookup_expr='gte',
        label='Monto pagado mínimo'
    )
    
    paid_amount_max = filters.NumberFilter(
        field_name='paid_amount',
        lookup_expr='lte',
        label='Monto pagado máximo'
    )
    
    balance_min = filters.NumberFilter(
        field_name='balance',
        lookup_expr='gte',
        label='Saldo mínimo'
    )
    
    balance_max = filters.NumberFilter(
        field_name='balance',
        lookup_expr='lte',
        label='Saldo máximo'
    )
    
    # Filtros por contrato
    has_contract = filters.BooleanFilter(
        field_name='contract',
        lookup_expr='isnull',
        exclude=True,
        label='Tiene contrato'
    )
    
    contract_number = filters.CharFilter(
        field_name='contract__contract_number',
        lookup_expr='icontains',
        label='Número de contrato'
    )
    
    # Filtros especiales
    overdue = filters.BooleanFilter(
        method='filter_overdue',
        label='Pedidos atrasados'
    )
    
    upcoming_deliveries = filters.BooleanFilter(
        method='filter_upcoming_deliveries',
        label='Próximas entregas (7 días)'
    )
    
    # Filtros por número de pedido
    order_number = filters.CharFilter(
        field_name='order_number',
        lookup_expr='icontains',
        label='Número de pedido'
    )
    
    # Filtros por campos específicos del cliente
    grade = filters.CharFilter(
        field_name='grade',
        lookup_expr='icontains',
        label='Grado'
    )
    
    section = filters.CharFilter(
        field_name='section',
        lookup_expr='icontains',
        label='Sección'
    )
    
    company_name = filters.CharFilter(
        field_name='client__company_name',
        lookup_expr='icontains',
        label='Nombre de empresa'
    )
    
    def filter_by_search(self, queryset, name, value):
        """Filtro de búsqueda general"""
        if value:
            return queryset.filter(
                Q(order_number__icontains=value) |
                Q(client__first_name__icontains=value) |
                Q(client__last_name__icontains=value) |
                Q(client__email__icontains=value) |
                Q(client__phone__icontains=value) |
                Q(client__dni__icontains=value) |
                Q(client__company_name__icontains=value)
            )
        return queryset
    
    def filter_by_date_range(self, queryset, name, value):
        """Filtro por rango de fechas"""
        if value:
            try:
                dates = value.split(',')
                if len(dates) == 2:
                    start_date = datetime.strptime(dates[0].strip(), '%Y-%m-%d').date()
                    end_date = datetime.strptime(dates[1].strip(), '%Y-%m-%d').date()
                    return queryset.filter(
                        Q(start_date__range=[start_date, end_date]) |
                        Q(delivery_date__range=[start_date, end_date])
                    )
            except (ValueError, IndexError):
                pass
        return queryset
    
    def filter_overdue(self, queryset, name, value):
        """Filtro de pedidos atrasados"""
        if value:
            today = datetime.now().date()
            return queryset.filter(
                delivery_date__lt=today,
                status__in=['pending', 'in_process']
            )
        return queryset
    
    def filter_upcoming_deliveries(self, queryset, name, value):
        """Filtro de próximas entregas"""
        if value:
            today = datetime.now().date()
            next_week = today + timedelta(days=7)
            return queryset.filter(
                delivery_date__range=[today, next_week],
                status__in=['pending', 'in_process']
            ).order_by('delivery_date')
        return queryset
    
    class Meta:
        model = Order
        fields = [
            'client_name', 'client_last_name', 'client_email', 'client_phone', 'client_dni',
            'search', 'document_type', 'status', 'client_type', 'school_level',
            'start_date_from', 'start_date_to', 'delivery_date_from', 'delivery_date_to',
            'date_range', 'total_min', 'total_max', 'paid_amount_min', 'paid_amount_max',
            'balance_min', 'balance_max', 'has_contract', 'contract_number',
            'overdue', 'upcoming_deliveries', 'order_number', 'grade', 'section', 'company_name'
        ]


class OrderItemFilter(filters.FilterSet):
    """
    Filtros para el modelo OrderItem
    
    Permite filtrar items de pedido por:
    - Pedido
    - Producto
    - Precio
    - Cantidad
    """
    
    order_number = filters.CharFilter(
        field_name='order__order_number',
        lookup_expr='icontains',
        label='Número de pedido'
    )
    
    order_status = filters.ChoiceFilter(
        field_name='order__status',
        choices=Order.ORDER_STATUS_CHOICES,
        label='Estado del pedido'
    )
    
    product_name = filters.CharFilter(
        field_name='product_name',
        lookup_expr='icontains',
        label='Nombre del producto'
    )
    
    quantity_min = filters.NumberFilter(
        field_name='quantity',
        lookup_expr='gte',
        label='Cantidad mínima'
    )
    
    quantity_max = filters.NumberFilter(
        field_name='quantity',
        lookup_expr='lte',
        label='Cantidad máxima'
    )
    
    unit_price_min = filters.NumberFilter(
        field_name='unit_price',
        lookup_expr='gte',
        label='Precio unitario mínimo'
    )
    
    unit_price_max = filters.NumberFilter(
        field_name='unit_price',
        lookup_expr='lte',
        label='Precio unitario máximo'
    )
    
    subtotal_min = filters.NumberFilter(
        field_name='subtotal',
        lookup_expr='gte',
        label='Subtotal mínimo'
    )
    
    subtotal_max = filters.NumberFilter(
        field_name='subtotal',
        lookup_expr='lte',
        label='Subtotal máximo'
    )
    
    affects_inventory = filters.BooleanFilter(
        field_name='affects_inventory',
        label='Afecta inventario'
    )
    
    class Meta:
        model = OrderItem
        fields = [
            'order_number', 'order_status', 'product_name',
            'quantity_min', 'quantity_max', 'unit_price_min', 'unit_price_max',
            'subtotal_min', 'subtotal_max', 'affects_inventory'
        ]


class ProductFilter(filters.FilterSet):
    """
    Filtros para el modelo Product
    
    Permite filtrar productos por:
    - Nombre y descripción
    - Tipo de producto
    - Precio
    - Stock
    - Estado activo
    """
    
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Nombre del producto'
    )
    
    description = filters.CharFilter(
        field_name='description',
        lookup_expr='icontains',
        label='Descripción'
    )
    
    product_type = filters.ChoiceFilter(
        field_name='product_type',
        choices=Product.PRODUCT_TYPE_CHOICES,
        label='Tipo de producto'
    )
    
    unit_price_min = filters.NumberFilter(
        field_name='unit_price',
        lookup_expr='gte',
        label='Precio unitario mínimo'
    )
    
    unit_price_max = filters.NumberFilter(
        field_name='unit_price',
        lookup_expr='lte',
        label='Precio unitario máximo'
    )
    
    stock_quantity_min = filters.NumberFilter(
        field_name='stock_quantity',
        lookup_expr='gte',
        label='Stock mínimo'
    )
    
    stock_quantity_max = filters.NumberFilter(
        field_name='stock_quantity',
        lookup_expr='lte',
        label='Stock máximo'
    )
    
    is_active = filters.BooleanFilter(
        field_name='is_active',
        label='Activo'
    )
    
    low_stock = filters.BooleanFilter(
        method='filter_low_stock',
        label='Bajo stock'
    )
    
    def filter_low_stock(self, queryset, name, value):
        """Filtro de productos con bajo stock"""
        if value:
            return queryset.filter(
                stock_quantity__lte=F('min_stock'),
                is_active=True
            )
        return queryset
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'product_type',
            'unit_price_min', 'unit_price_max',
            'stock_quantity_min', 'stock_quantity_max',
            'is_active', 'low_stock'
        ]