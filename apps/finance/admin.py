# apps/finance/admin.py

from django.contrib import admin
# Importamos los modelos desde el ARCHIVO ÍNDICE de la misma carpeta (finance/models.py)
from .models import (
    ExpenseCategory, 
    PersonalExpense, 
    ServiceExpense, 
    Budget
)

### Definiciones de Clases Admin ###

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    """ Registro para Categorías de Gastos """
    list_display = ('nombre', 'is_active', 'tenant', 'created_at')
    list_filter = ('is_active', 'tenant')
    search_fields = ('nombre', 'descripcion')

@admin.register(PersonalExpense)
class PersonalExpenseAdmin(admin.ModelAdmin):
    """ Registro para Gastos de Personal (Nómina) """
    list_display = ('nombre', 'cargo', 'salario_base', 'bonificaciones', 'descuentos', 'estado', 'fecha_pago', 'tenant')
    list_filter = ('estado', 'cargo', 'fecha_pago')
    search_fields = ('nombre', 'codigo')
    readonly_fields = ('salario_neto',) # Muestra el @property en el admin

@admin.register(ServiceExpense)
class ServiceExpenseAdmin(admin.ModelAdmin):
    """ Registro para Gastos de Servicio (Luz, Agua, etc.) """
    list_display = ('proveedor', 'tipo', 'monto', 'estado', 'fecha_vencimiento', 'periodo', 'tenant')
    list_filter = ('estado', 'tipo', 'proveedor')
    search_fields = ('proveedor', 'codigo')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    """ Registro para Presupuestos por Categoría """
    list_display = ('categoria', 'monto_presupuestado', 'periodo_inicio', 'periodo_fin', 'tenant')
    list_filter = ('categoria', 'periodo_inicio')
    search_fields = ('categoria__nombre',)
    # readonly_fields = ('balance', 'porcentaje_gastado') # Campos calculados si se muestran en admin