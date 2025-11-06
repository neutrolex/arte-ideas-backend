from django.contrib import admin
from django.contrib import messages
from datetime import date, timedelta
from decimal import Decimal
from .models import Activo, Financiamiento, Mantenimiento, Repuesto

# Register your models here.

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo_total', 'categoria', 'proveedor', 'fecha_compra', 'tipo_pago', 'vida_util', 'depreciacion_mensual', 'estado')
    list_filter = ('categoria', 'tipo_pago', 'estado', 'proveedor')
    search_fields = ('nombre', 'proveedor')
    
    def save_model(self, request, obj, form, change):
        """Sobrescribir save_model para manejar financiamientos automáticamente"""
        super().save_model(request, obj, form, change)
        
        # Si el activo es financiado o leasing, crear/actualizar financiamiento
        if obj.tipo_pago in ['financiado', 'leasing']:
            financiamiento, created = Financiamiento.objects.get_or_create(
                activo=obj,
                defaults={
                    'tipo_pago': obj.tipo_pago,
                    'entidad_financiera': 'Por definir',
                    'monto_financiado': obj.costo_total * Decimal('0.8') if obj.tipo_pago == 'financiado' else obj.costo_total,
                    'cuotas_totales': 24 if obj.tipo_pago == 'financiado' else 60,
                    'cuota_mensual': (obj.costo_total * Decimal('0.8')) / 24 if obj.tipo_pago == 'financiado' else obj.costo_total / 60,
                    'fecha_inicio': date.today(),
                    'fecha_fin': date.today() + timedelta(days=730) if obj.tipo_pago == 'financiado' else date.today() + timedelta(days=1825),
                    'estado': 'activo'
                }
            )
            
            if created:
                messages.success(request, f'✅ Registro de financiamiento creado automáticamente para {obj.nombre}')
            else:
                # Actualizar tipo de pago si cambió
                financiamiento.tipo_pago = obj.tipo_pago
                financiamiento.save()
                messages.info(request, f'ℹ️ Registro de financiamiento actualizado para {obj.nombre}')
        else:
            # Si ya no es financiado, eliminar financiamiento existente
            deleted_count = Financiamiento.objects.filter(activo=obj).delete()[0]
            if deleted_count > 0:
                messages.warning(request, f'⚠️ Registro de financiamiento eliminado para {obj.nombre} (ya no es financiado)')

@admin.register(Financiamiento)
class FinanciamientoAdmin(admin.ModelAdmin):
    list_display = ('activo', 'tipo_pago', 'entidad_financiera', 'monto_financiado', 'cuota_mensual', 'cuotas_totales', 'estado')
    list_filter = ('tipo_pago', 'estado', 'entidad_financiera')
    search_fields = ('activo__nombre', 'entidad_financiera')
    readonly_fields = ('activo',)  # No permitir cambiar el activo desde aquí
    
    def get_queryset(self, request):
        """Solo mostrar financiamientos de activos que realmente son financiados/leasing"""
        return super().get_queryset(request).filter(activo__tipo_pago__in=['financiado', 'leasing'])

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('activo', 'proxima_fecha_mantenimiento', 'tipo_mantenimiento', 'fecha_mantenimiento', 'proveedor', 'costo', 'descripcion', 'estado_del_mantenimiento','estado_del_activo')

@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'ubicacion', 'proveedor', 'stock_actual', 'stock_minimo', 'costo_unitario', 'descripcion')
