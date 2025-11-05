from django.contrib import admin
from .models import (
    MolduraListon, MolduraPrearmada, VidrioTapaMDF, Paspartu,
    Minilab, Cuadro, Anuario, CorteLaser, MarcoAccesorio, HerramientaGeneral
)


class BaseInventarioAdmin(admin.ModelAdmin):
    """Admin base para todos los modelos de inventario"""
    list_display = ['nombre_producto', 'stock_disponible', 'stock_minimo', 'costo_unitario', 'costo_total', 'alerta_stock']
    list_filter = ['fecha_creacion', 'fecha_actualizacion']
    search_fields = ['nombre_producto']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'costo_total', 'alerta_stock']
    
    def alerta_stock(self, obj):
        return "⚠️ ALERTA" if obj.alerta_stock else "✅ OK"
    alerta_stock.short_description = "Estado Stock"
    
    def costo_total(self, obj):
        return f"S/ {obj.costo_total:.2f}"
    costo_total.short_description = "Costo Total"


@admin.register(MolduraListon)
class MolduraListonAdmin(BaseInventarioAdmin):
    list_display = BaseInventarioAdmin.list_display + ['nombre_moldura', 'ancho', 'color', 'material']
    list_filter = BaseInventarioAdmin.list_filter + ['nombre_moldura', 'material', 'color']
    fieldsets = (
        ('Información del Producto', {
            'fields': ('nombre_producto', 'nombre_moldura', 'ancho', 'color', 'material')
        }),
        ('Stock y Costos', {
            'fields': ('stock_disponible', 'stock_minimo', 'costo_unitario')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion', 'fecha_actualizacion', 'costo_total', 'alerta_stock'),
            'classes': ('collapse',)
        })
    )


@admin.register(MolduraPrearmada)
class MolduraPrearmadaAdmin(BaseInventarioAdmin):
    list_display = BaseInventarioAdmin.list_display + ['dimensiones', 'color', 'material']
    list_filter = BaseInventarioAdmin.list_filter + ['dimensiones', 'material', 'color']


@admin.register(VidrioTapaMDF)
class VidrioTapaMDFAdmin(BaseInventarioAdmin):
    list_display = BaseInventarioAdmin.list_display + ['tipo_material', 'tipo_vidrio', 'grosor', 'tamaño']
    list_filter = BaseInventarioAdmin.list_filter + ['tipo_material', 'grosor', 'tamaño']


@admin.register(Paspartu)
class PaspartuAdmin(BaseInventarioAdmin):
    list_display = BaseInventarioAdmin.list_display + ['tipo_material', 'tamaño', 'grosor', 'color']
    list_filter = BaseInventarioAdmin.list_filter + ['tipo_material', 'color', 'grosor']


@admin.register(Minilab)
class MinilabAdmin(BaseInventarioAdmin):
    list_display = BaseInventarioAdmin.list_display + ['tipo_insumo', 'nombre_tipo', 'tamaño_presentacion', 'fecha_compra']
    list_filter = BaseInventarioAdmin.list_filter + ['tipo_insumo', 'nombre_tipo', 'fecha_compra']


@admin.register(Cuadro)
class CuadroAdmin(BaseInventarioAdmin):
    list_display = BaseInventarioAdmin.list_display + ['formato', 'dimensiones', 'material']
    list_filter = BaseInventarioAdmin.list_filter + ['formato', 'material', 'dimensiones']


@admin.register(Anuario)
class AnuarioAdmin(BaseInventarioAdmin):
    list_display = BaseInventarioAdmin.list_display + ['formato', 'paginas', 'tipo_tapa']
    list_filter = BaseInventarioAdmin.list_filter + ['formato', 'paginas', 'tipo_tapa']


@admin.register(CorteLaser)
class CorteLaserAdmin(BaseInventarioAdmin):
    list_display = BaseInventarioAdmin.list_display + ['producto', 'tipo', 'tamaño', 'color', 'unidad']
    list_filter = BaseInventarioAdmin.list_filter + ['producto', 'tipo', 'color', 'unidad']


@admin.register(MarcoAccesorio)
class MarcoAccesorioAdmin(BaseInventarioAdmin):
    list_display = BaseInventarioAdmin.list_display + ['tipo_moldura', 'material', 'color', 'dimensiones']
    list_filter = BaseInventarioAdmin.list_filter + ['tipo_moldura', 'material', 'color']


@admin.register(HerramientaGeneral)
class HerramientaGeneralAdmin(BaseInventarioAdmin):
    list_display = BaseInventarioAdmin.list_display + ['marca', 'tipo_material']
    list_filter = BaseInventarioAdmin.list_filter + ['marca', 'tipo_material']