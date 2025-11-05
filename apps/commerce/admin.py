"""
Admin configuration for Commerce App - Arte Ideas
Configuración del panel de administración para modelos de comercio
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.db.models import Sum, F, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Administración de Productos"""
    
    list_display = [
        'name', 'product_type', 'unit_price', 'stock_quantity', 'is_active',
        'low_stock_indicator', 'created_at_formatted'
    ]
    list_filter = [
        'product_type', 'is_active', 'created_at', 'updated_at'
    ]
    search_fields = [
        'name', 'description', 'sku'
    ]
    list_editable = ['unit_price', 'stock_quantity', 'is_active']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'product_type', 'sku')
        }),
        ('Precio y Stock', {
            'fields': ('unit_price', 'stock_quantity', 'is_active')
        }),
        ('Imágenes', {
            'fields': ('image', 'image_preview')
        }),
        ('Información Adicional', {
            'fields': ('notes',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['image_preview', 'created_at_formatted', 'updated_at_formatted']
    
    def low_stock_indicator(self, obj):
        """Indicador visual de stock bajo"""
        if obj.stock_quantity <= 5:
            return mark_safe('<span style="color: red; font-weight: bold;">⚠️ Stock Bajo</span>')
        elif obj.stock_quantity <= 10:
            return mark_safe('<span style="color: orange;">⚡ Stock Medio</span>')
        else:
            return mark_safe('<span style="color: green;">✅ Stock Alto</span>')
    
    low_stock_indicator.short_description = 'Estado Stock'
    
    def image_preview(self, obj):
        """Vista previa de imagen del producto"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" style="object-fit: cover;" />')
        return mark_safe('<span style="color: gray;">Sin imagen</span>')
    
    image_preview.short_description = 'Vista Previa'
    
    def created_at_formatted(self, obj):
        """Fecha de creación formateada"""
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    
    created_at_formatted.short_description = 'Creado el'
    
    def updated_at_formatted(self, obj):
        """Fecha de actualización formateada"""
        return obj.updated_at.strftime('%d/%m/%Y %H:%M') if obj.updated_at else '-'
    
    updated_at_formatted.short_description = 'Actualizado el'
    
    actions = ['mark_as_active', 'mark_as_inactive', 'update_low_stock_prices']
    
    def mark_as_active(self, request, queryset):
        """Marcar productos como activos"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} producto(s) marcado(s) como activo(s).', messages.SUCCESS)
    
    mark_as_active.short_description = "Marcar como activos"
    
    def mark_as_inactive(self, request, queryset):
        """Marcar productos como inactivos"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} producto(s) marcado(s) como inactivo(s).', messages.WARNING)
    
    mark_as_inactive.short_description = "Marcar como inactivos"
    
    def update_low_stock_prices(self, request, queryset):
        """Actualizar precios de productos con stock bajo"""
        low_stock_products = queryset.filter(stock_quantity__lte=5)
        if low_stock_products.exists():
            count = low_stock_products.count()
            self.message_user(
                request, 
                f'{count} producto(s) con stock bajo identificado(s). Considerar actualizar precios o reabastecer.',
                messages.WARNING
            )
        else:
            self.message_user(request, 'No hay productos con stock bajo.', messages.INFO)
    
    update_low_stock_prices.short_description = "Verificar productos con stock bajo"


class OrderItemInline(admin.TabularInline):
    """Inline para OrderItems en la vista de Order"""
    model = OrderItem
    extra = 0
    fields = ['product', 'quantity', 'unit_price', 'subtotal', 'inventory_impact']
    readonly_fields = ['subtotal']
    
    def subtotal(self, obj):
        """Calcular subtotal"""
        return f"S/. {obj.quantity * obj.unit_price:.2f}"
    
    subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Administración de Órdenes"""
    
    list_display = [
        'order_number', 'client_link', 'document_type', 'status',
        'total', 'balance', 'delivery_date', 'status_indicator',
        'created_at_formatted'
    ]
    list_filter = [
        'status', 'document_type', 'client_type', 'created_at',
        'delivery_date'
    ]
    search_fields = [
        'order_number', 'client__first_name', 'client__last_name',
        'client__company_name', 'client__ruc', 'client__dni'
    ]
    list_editable = ['status']
    ordering = ['-created_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Información de la Orden', {
            'fields': (
                'order_number', 'status', 'document_type', 'client_type',
                'client', 'contract', 'description'
            )
        }),
        ('Información de Entrega', {
            'fields': (
                'delivery_date', 'delivery_address', 'delivery_notes'
            )
        }),
        ('Información de Pago', {
            'fields': (
                'total_amount', 'advance_payment', 'balance',
                'payment_method', 'payment_status'
            )
        }),
        ('Información Adicional', {
            'fields': (
                'notes', 'school_level', 'school_grade', 'school_section'
            ),
            'classes': ('collapse',)
        }),
        ('Estado y Auditoría', {
            'fields': (
                'created_at_formatted', 'updated_at_formatted'
            ),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = [
        'order_number', 'balance', 'created_at_formatted', 'updated_at_formatted', 'status_indicator'
    ]
    
    def client_link(self, obj):
        """Enlace al cliente"""
        if obj.client:
            url = reverse('admin:crm_client_change', args=[obj.client.id])
            return format_html('<a href="{}">{}</a>', url, str(obj.client))
        return '-'
    
    client_link.short_description = 'Cliente'
    
    def status_indicator(self, obj):
        """Indicador visual de estado"""
        status_colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'in_progress': 'purple',
            'completed': 'green',
            'cancelled': 'red',
            'delayed': 'red'
        }
        
        status_labels = {
            'pending': 'Pendiente',
            'confirmed': 'Confirmado',
            'in_progress': 'En Proceso',
            'completed': 'Completado',
            'cancelled': 'Cancelado',
            'delayed': 'Atrasado'
        }
        
        color = status_colors.get(obj.status, 'gray')
        label = status_labels.get(obj.status, obj.status)
        
        if obj.status == 'atrasado' and obj.status not in ['completed', 'cancelled']:
            return mark_safe(f'<span style="color: red; font-weight: bold;">⚠️ {label} (Atrasado)</span>')
        
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">● {label}</span>')
    
    status_indicator.short_description = 'Estado'
    
    def created_at_formatted(self, obj):
        """Fecha de creación formateada"""
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    
    created_at_formatted.short_description = 'Creado el'
    
    def updated_at_formatted(self, obj):
        """Fecha de actualización formateada"""
        return obj.updated_at.strftime('%d/%m/%Y %H:%M') if obj.updated_at else '-'
    
    updated_at_formatted.short_description = 'Actualizado el'
    
    def get_queryset(self, request):
        """Sobrescribir queryset para optimizar"""
        qs = super().get_queryset(request)
        return qs.select_related('client', 'contract').prefetch_related('items')
    
    def save_model(self, request, obj, form, change):
        """Guardar modelo con usuario actual"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = [
        'mark_as_completed', 'mark_as_cancelled', 'mark_as_confirmed',
        'mark_as_in_progress', 'check_overdue_orders', 'generate_delivery_report'
    ]
    
    def mark_as_completed(self, request, queryset):
        """Marcar órdenes como completadas"""
        updated = queryset.filter(status__in=['pending', 'confirmed', 'in_progress']).update(status='completed')
        self.message_user(request, f'{updated} orden(es) marcada(s) como completada(s).', messages.SUCCESS)
    
    mark_as_completed.short_description = "Marcar como completadas"
    
    def mark_as_cancelled(self, request, queryset):
        """Marcar órdenes como canceladas"""
        updated = queryset.exclude(status='completed').update(status='cancelled')
        self.message_user(request, f'{updated} orden(es) marcada(s) como cancelada(s).', messages.WARNING)
    
    mark_as_cancelled.short_description = "Marcar como canceladas"
    
    def mark_as_confirmed(self, request, queryset):
        """Marcar órdenes como confirmadas"""
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'{updated} orden(es) marcada(s) como confirmada(s).', messages.INFO)
    
    mark_as_confirmed.short_description = "Marcar como confirmadas"
    
    def mark_as_in_progress(self, request, queryset):
        """Marcar órdenes como en proceso"""
        updated = queryset.filter(status__in=['pending', 'confirmed']).update(status='in_progress')
        self.message_user(request, f'{updated} orden(es) marcada(s) como en proceso.', messages.INFO)
    
    mark_as_in_progress.short_description = "Marcar como en proceso"
    
    def check_overdue_orders(self, request, queryset):
        """Verificar órdenes atrasadas"""
        today = timezone.now().date()
        overdue_orders = queryset.filter(
            delivery_date__lt=today,
            status__in=['pending', 'confirmed', 'in_progress']
        )
        
        if overdue_orders.exists():
            count = overdue_orders.update(status='atrasado')
            self.message_user(
                request,
                f'{count} orden(es) marcada(s) como atrasada(s).',
                messages.WARNING
            )
        else:
            self.message_user(request, 'No hay órdenes atrasadas.', messages.INFO)
    
    check_overdue_orders.short_description = "Verificar órdenes atrasadas"
    
    def generate_delivery_report(self, request, queryset):
        """Generar reporte de entregas"""
        today = timezone.now().date()
        upcoming_deliveries = queryset.filter(
            delivery_date__gte=today,
            delivery_date__lte=today + timedelta(days=7),
            status__in=['pending', 'confirmed', 'in_progress']
        ).count()
        
        overdue_deliveries = queryset.filter(
            delivery_date__lt=today,
            status__in=['pending', 'confirmed', 'in_progress']
        ).count()
        
        self.message_user(
            request,
            f'Reporte de entregas: {upcoming_deliveries} entregas próximas (7 días), {overdue_deliveries} entregas atrasadas.',
            messages.INFO
        )
    
    generate_delivery_report.short_description = "Generar reporte de entregas"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Administración de Items de Órdenes"""
    
    list_display = [
        'order_link', 'product_name', 'quantity', 'unit_price',
        'subtotal', 'created_at_formatted'
    ]
    list_filter = [
        'created_at'
    ]
    search_fields = [
        'order__order_number', 'product__name', 'product__sku'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información del Item', {
            'fields': ('order', 'product', 'quantity', 'unit_price')
        }),
        ('Auditoría', {
            'fields': ('created_at_formatted', 'updated_at_formatted'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = [
        'created_at_formatted', 'updated_at_formatted'
    ]
    
    def order_link(self, obj):
        """Enlace a la orden"""
        if obj.order:
            url = reverse('admin:commerce_order_change', args=[obj.order.id])
            return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
        return '-'
    
    order_link.short_description = 'Orden'
    
    def subtotal(self, obj):
        """Calcular subtotal"""
        return f"S/. {obj.quantity * obj.unit_price:.2f}"
    
    subtotal.short_description = 'Subtotal'
    
    def created_at_formatted(self, obj):
        """Fecha de creación formateada"""
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    
    created_at_formatted.short_description = 'Creado el'
    
    def updated_at_formatted(self, obj):
        """Fecha de actualización formateada"""
        return obj.updated_at.strftime('%d/%m/%Y %H:%M') if obj.updated_at else '-'
    
    updated_at_formatted.short_description = 'Actualizado el'
    
    def get_queryset(self, request):
        """Sobrescribir queryset para optimizar"""
        qs = super().get_queryset(request)
        return qs.select_related('order', 'product')


# Configuración adicional del admin
admin.site.site_header = 'Arte Ideas - Administración'
admin.site.site_title = 'Arte Ideas'
admin.site.index_title = 'Panel de Administración'