"""
Administración del Módulo de Inventario - Arte Ideas Commerce
"""
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum

from .models import (
    MolduraListon, MolduraPrearmada, VidrioTapaMDF, Paspartu,
    Minilab, Cuadro, Anuario, CorteLaser, MarcoAccesorio, HerramientaGeneral
)


class BaseInventarioAdmin(admin.ModelAdmin):
    """Administración base para todos los modelos de inventario"""
    list_display = [
        'nombre_producto', 'stock_badge', 'stock_minimo',
        'costo_unitario', 'precio_venta', 'costo_total_display',
        'proveedor', 'is_active'
    ]
    list_filter = ['is_active', 'proveedor', 'fecha_ultima_compra']
    search_fields = ['nombre_producto', 'codigo_producto', 'proveedor']
    readonly_fields = ['costo_total', 'alerta_stock', 'fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'nombre_producto', 'codigo_producto', 'ubicacion'
            )
        }),
        ('Stock', {
            'fields': (
                'stock_disponible', 'stock_minimo', 'alerta_stock'
            )
        }),
        ('Precios', {
            'fields': (
                'costo_unitario', 'precio_venta', 'costo_total'
            )
        }),
        ('Proveedor', {
            'fields': (
                'proveedor', 'fecha_ultima_compra'
            )
        }),
        ('Estado', {
            'fields': (
                'is_active',
            )
        }),
        ('Metadatos', {
            'fields': (
                'fecha_creacion', 'fecha_actualizacion'
            ),
            'classes': ('collapse',)
        })
    )
    
    def stock_badge(self, obj):
        """Mostrar stock con badge de color según nivel"""
        if obj.alerta_stock:
            color = '#dc3545'  # Rojo para alerta
            icon = '⚠️'
        elif obj.stock_disponible <= obj.stock_minimo * 1.5:
            color = '#ffc107'  # Amarillo para advertencia
            icon = '⚡'
        else:
            color = '#28a745'  # Verde para normal
            icon = '✅'
        
        return format_html(
            '{} <span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            icon,
            color,
            obj.stock_disponible
        )
    stock_badge.short_description = 'Stock Disponible'
    
    def costo_total_display(self, obj):
        """Mostrar costo total formateado"""
        return f'S/ {obj.costo_total:,.2f}'
    costo_total_display.short_description = 'Costo Total'
    
    def get_queryset(self, request):
        """Filtrar por tenant del usuario"""
        qs = super().get_queryset(request)
        if hasattr(request.user, 'tenant'):
            return qs.filter(tenant=request.user.tenant)
        return qs
    
    def save_model(self, request, obj, form, change):
        """Guardar con tenant actual"""
        if not change:  # Solo en creación
            obj.tenant = request.user.tenant
        super().save_model(request, obj, form, change)


# CATEGORÍA: ENMARCADOS
@admin.register(MolduraListon)
class MolduraListonAdmin(BaseInventarioAdmin):
    """Administración de Moldura (Listón)"""
    list_display = BaseInventarioAdmin.list_display + [
        'nombre_moldura', 'ancho', 'color', 'material'
    ]
    list_filter = BaseInventarioAdmin.list_filter + [
        'nombre_moldura', 'ancho', 'color', 'material'
    ]
    
    fieldsets = BaseInventarioAdmin.fieldsets[:1] + (
        ('Especificaciones', {
            'fields': (
                'nombre_moldura', 'ancho', 'color', 'material'
            )
        }),
    ) + BaseInventarioAdmin.fieldsets[1:]


@admin.register(MolduraPrearmada)
class MolduraPrearmadaAdmin(BaseInventarioAdmin):
    """Administración de Moldura Prearmada"""
    list_display = BaseInventarioAdmin.list_display + [
        'dimensiones', 'color', 'material'
    ]
    list_filter = BaseInventarioAdmin.list_filter + [
        'dimensiones', 'color', 'material'
    ]
    
    fieldsets = BaseInventarioAdmin.fieldsets[:1] + (
        ('Especificaciones', {
            'fields': (
                'dimensiones', 'color', 'material'
            )
        }),
    ) + BaseInventarioAdmin.fieldsets[1:]


@admin.register(VidrioTapaMDF)
class VidrioTapaMDFAdmin(BaseInventarioAdmin):
    """Administración de Vidrio o Tapa MDF"""
    list_display = BaseInventarioAdmin.list_display + [
        'tipo_material', 'tipo_vidrio', 'grosor', 'tamaño'
    ]
    list_filter = BaseInventarioAdmin.list_filter + [
        'tipo_material', 'tipo_vidrio', 'grosor', 'tamaño'
    ]
    
    fieldsets = BaseInventarioAdmin.fieldsets[:1] + (
        ('Especificaciones', {
            'fields': (
                'tipo_material', 'tipo_vidrio', 'grosor', 'tamaño'
            )
        }),
    ) + BaseInventarioAdmin.fieldsets[1:]


@admin.register(Paspartu)
class PaspartuAdmin(BaseInventarioAdmin):
    """Administración de Paspartú"""
    list_display = BaseInventarioAdmin.list_display + [
        'tipo_material', 'tamaño', 'grosor', 'color'
    ]
    list_filter = BaseInventarioAdmin.list_filter + [
        'tipo_material', 'tamaño', 'grosor', 'color'
    ]
    
    fieldsets = BaseInventarioAdmin.fieldsets[:1] + (
        ('Especificaciones', {
            'fields': (
                'tipo_material', 'tamaño', 'grosor', 'color'
            )
        }),
    ) + BaseInventarioAdmin.fieldsets[1:]


# CATEGORÍA: MINILAB
@admin.register(Minilab)
class MinilabAdmin(BaseInventarioAdmin):
    """Administración de Minilab"""
    list_display = BaseInventarioAdmin.list_display + [
        'tipo_insumo', 'nombre_tipo', 'tamaño_presentacion', 'fecha_compra'
    ]
    list_filter = BaseInventarioAdmin.list_filter + [
        'tipo_insumo', 'nombre_tipo', 'tamaño_presentacion', 'fecha_compra'
    ]
    
    fieldsets = BaseInventarioAdmin.fieldsets[:1] + (
        ('Especificaciones', {
            'fields': (
                'tipo_insumo', 'nombre_tipo', 'tamaño_presentacion', 'fecha_compra'
            )
        }),
    ) + BaseInventarioAdmin.fieldsets[1:]


# CATEGORÍA: GRADUACIONES
@admin.register(Cuadro)
class CuadroAdmin(BaseInventarioAdmin):
    """Administración de Cuadro"""
    list_display = BaseInventarioAdmin.list_display + [
        'formato', 'dimensiones', 'material'
    ]
    list_filter = BaseInventarioAdmin.list_filter + [
        'formato', 'dimensiones', 'material'
    ]
    
    fieldsets = BaseInventarioAdmin.fieldsets[:1] + (
        ('Especificaciones', {
            'fields': (
                'formato', 'dimensiones', 'material'
            )
        }),
    ) + BaseInventarioAdmin.fieldsets[1:]


@admin.register(Anuario)
class AnuarioAdmin(BaseInventarioAdmin):
    """Administración de Anuario"""
    list_display = BaseInventarioAdmin.list_display + [
        'formato', 'paginas', 'tipo_tapa'
    ]
    list_filter = BaseInventarioAdmin.list_filter + [
        'formato', 'paginas', 'tipo_tapa'
    ]
    
    fieldsets = BaseInventarioAdmin.fieldsets[:1] + (
        ('Especificaciones', {
            'fields': (
                'formato', 'paginas', 'tipo_tapa'
            )
        }),
    ) + BaseInventarioAdmin.fieldsets[1:]


# CATEGORÍA: CORTE LÁSER
@admin.register(CorteLaser)
class CorteLaserAdmin(BaseInventarioAdmin):
    """Administración de Corte Láser"""
    list_display = BaseInventarioAdmin.list_display + [
        'producto', 'tipo', 'tamaño', 'color', 'unidad'
    ]
    list_filter = BaseInventarioAdmin.list_filter + [
        'producto', 'tipo', 'tamaño', 'color', 'unidad'
    ]
    
    fieldsets = BaseInventarioAdmin.fieldsets[:1] + (
        ('Especificaciones', {
            'fields': (
                'producto', 'tipo', 'tamaño', 'color', 'unidad'
            )
        }),
    ) + BaseInventarioAdmin.fieldsets[1:]


# CATEGORÍA: ACCESORIOS
@admin.register(MarcoAccesorio)
class MarcoAccesorioAdmin(BaseInventarioAdmin):
    """Administración de Marco y Accesorio"""
    list_display = BaseInventarioAdmin.list_display + [
        'nombre_moldura', 'tipo_moldura', 'material', 'color'
    ]
    list_filter = BaseInventarioAdmin.list_filter + [
        'tipo_moldura', 'material', 'color'
    ]
    
    fieldsets = BaseInventarioAdmin.fieldsets[:1] + (
        ('Especificaciones', {
            'fields': (
                'nombre_moldura', 'tipo_moldura', 'material', 'color', 'dimensiones'
            )
        }),
    ) + BaseInventarioAdmin.fieldsets[1:]


@admin.register(HerramientaGeneral)
class HerramientaGeneralAdmin(BaseInventarioAdmin):
    """Administración de Herramienta General"""
    list_display = BaseInventarioAdmin.list_display + [
        'nombre_herramienta', 'marca', 'tipo_material'
    ]
    list_filter = BaseInventarioAdmin.list_filter + [
        'marca', 'tipo_material'
    ]
    
    fieldsets = BaseInventarioAdmin.fieldsets[:1] + (
        ('Especificaciones', {
            'fields': (
                'nombre_herramienta', 'marca', 'tipo_material'
            )
        }),
    ) + BaseInventarioAdmin.fieldsets[1:]