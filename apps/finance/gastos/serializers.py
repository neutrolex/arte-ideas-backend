from rest_framework import serializers
# --- CORRECCIÓN CLAVE ---
# Importaciones hacia el índice 'finance/models.py'
from ..models import (
    ExpenseCategory,
    PersonalExpense,
    ServiceExpense,
    Budget,
)


class ExpenseCategorySerializer(serializers.ModelSerializer):
    """ Serializer para el modelo ExpenseCategory. """
    class Meta:
        model = ExpenseCategory
        fields = [
            'id',
            'nombre',
            'descripcion',
            'is_active',
        ]
    

class PersonalExpenseSerializer(serializers.ModelSerializer):
    
    # Convierte a camelCase y usa @property salario_neto
    salarioNeto = serializers.DecimalField(
        source='salario_neto', 
        read_only=True, 
        max_digits=10, 
        decimal_places=2
    )
    salarioBase = serializers.DecimalField(
        source='salario_base', 
        max_digits=10, 
        decimal_places=2
    )
    fechaPago = serializers.DateField(source='fecha_pago', required=False, allow_null=True)
    
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=ExpenseCategory.objects.all(), 
        required=False
    )

    class Meta:
        model = PersonalExpense
        fields = [
            'id', 'codigo', 'nombre', 'cargo', 'salarioBase',      
            'bonificaciones', 'descuentos', 'fechaPago',        
            'estado', 'categoria', 'salarioNeto', 'created_at',
        ]
        read_only_fields = ['created_at']


class ServiceExpenseSerializer(serializers.ModelSerializer):
 
    # Convierte a camelCase
    tipoServicio = serializers.CharField(source='tipo')
    fechaVencimiento = serializers.DateField(source='fecha_vencimiento')
    fechaPago = serializers.DateField(source='fecha_pago', required=False, allow_null=True)
    
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=ExpenseCategory.objects.all(), 
        required=False
    )

    class Meta:
        model = ServiceExpense
        fields = [
            'id', 'codigo', 'tipoServicio', 'proveedor', 'monto',
            'fechaVencimiento', 'fechaPago', 'periodo', 'estado',
            'categoria', 'created_at',
        ]
        read_only_fields = ['created_at']


class BudgetSerializer(serializers.ModelSerializer):
 
    # Propiedades calculadas
    balance = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    porcentajeGastado = serializers.FloatField(source='porcentaje_gastado', read_only=True)
    
    # Conversiones a camelCase y campos relacionados
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=ExpenseCategory.objects.all()
    )
    periodoInicio = serializers.DateField(source='periodo_inicio')
    periodoFin = serializers.DateField(source='periodo_fin')
    montoPresupuestado = serializers.DecimalField(
        source='monto_presupuestado', max_digits=12, decimal_places=2
    )
    montoGastado = serializers.DecimalField(
        source='monto_gastado', max_digits=12, decimal_places=2, read_only=True
    )
    categoriaNombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Budget
        fields = [
            'id', 'categoria', 'categoriaNombre', 'periodoInicio',     
            'periodoFin', 'montoPresupuestado', 'montoGastado',      
            'balance', 'porcentajeGastado',  
        ]