"""
Serializadores del Commerce App - Arte Ideas
Serialización y validación de datos de pedidos
"""
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
import json

from apps.core.models import Tenant
from apps.crm.models import Client, Contract
from .models import Order, OrderItem, Product


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializador para items de pedido"""
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_description', 'quantity', 'unit_price', 'subtotal', 'affects_inventory']
        read_only_fields = ['id', 'subtotal', 'affects_inventory']
    
    def validate_quantity(self, value):
        """Validar cantidad"""
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value
    
    def validate_unit_price(self, value):
        """Validar precio unitario"""
        if value < 0:
            raise serializers.ValidationError("El precio unitario no puede ser negativo")
        return value


class OrderSerializer(serializers.ModelSerializer):
    """Serializador principal para pedidos"""
    items = OrderItemSerializer(many=True, required=False)
    client_info = serializers.SerializerMethodField()
    scheduled_sessions = serializers.SerializerMethodField()
    scheduled_deliveries = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'client', 'client_info', 'document_type', 'client_type',
            'school_level', 'grade', 'section', 'start_date', 'delivery_date',
            'scheduled_dates', 'scheduled_sessions', 'scheduled_deliveries',
            'subtotal', 'tax', 'total', 'paid_amount', 'balance', 'extra_services',
            'status', 'contract', 'notes', 'affects_inventory', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'balance', 'affects_inventory', 'created_at', 'updated_at']
    
    def get_client_info(self, obj):
        """Obtener información del cliente"""
        if obj.client:
            return {
                'id': obj.client.id,
                'full_name': obj.client.get_full_name(),
                'email': obj.client.email,
                'phone': obj.client.phone,
                'dni': obj.client.dni,
                'address': obj.client.address,
                'client_type': obj.client.client_type,
                'school_level': obj.client.school_level,
                'grade': obj.client.grade,
                'section': obj.client.section,
                'company_name': obj.client.company_name,
            }
        return None
    
    def get_scheduled_sessions(self, obj):
        """Obtener sesiones programadas"""
        return obj.get_scheduled_sessions()
    
    def get_scheduled_deliveries(self, obj):
        """Obtener entregas programadas"""
        return obj.get_scheduled_deliveries()
    
    def validate_order_number(self, value):
        """Validar número de pedido único por tenant"""
        tenant = self.context['request'].user.tenant
        if Order.objects.filter(order_number=value, tenant=tenant).exists():
            if self.instance and self.instance.order_number == value:
                return value  # Es la misma instancia, permitir
            raise serializers.ValidationError("Ya existe un pedido con este número")
        return value
    
    def validate_client(self, value):
        """Validar que el cliente existe y pertenece al tenant"""
        tenant = self.context['request'].user.tenant
        try:
            client = Client.objects.get(id=value.id, tenant=tenant)
            return client
        except Client.DoesNotExist:
            raise serializers.ValidationError("El cliente no existe o no pertenece a este estudio")
    
    def validate_document_type(self, value):
        """Validar tipo de documento"""
        valid_types = ['proforma', 'nota_venta', 'contrato']
        if value not in valid_types:
            raise serializers.ValidationError(f"Tipo de documento inválido. Opciones: {', '.join(valid_types)}")
        return value
    
    def validate_client_type(self, value):
        """Validar tipo de cliente"""
        valid_types = ['particular', 'colegio', 'empresa']
        if value not in valid_types:
            raise serializers.ValidationError(f"Tipo de cliente inválido. Opciones: {', '.join(valid_types)}")
        return value
    
    def validate_school_level(self, value):
        """Validar nivel escolar"""
        if value:
            valid_levels = ['inicial', 'primaria', 'secundaria']
            if value not in valid_levels:
                raise serializers.ValidationError(f"Nivel escolar inválido. Opciones: {', '.join(valid_levels)}")
        return value
    
    def validate_dates(self, data):
        """Validar fechas"""
        start_date = data.get('start_date')
        delivery_date = data.get('delivery_date')
        
        if start_date and delivery_date and start_date > delivery_date:
            raise serializers.ValidationError({
                'delivery_date': 'La fecha de entrega debe ser posterior a la fecha de inicio'
            })
        
        return data
    
    def validate_amounts(self, data):
        """Validar montos"""
        total = data.get('total', 0)
        paid_amount = data.get('paid_amount', 0)
        
        if total < 0:
            raise serializers.ValidationError({'total': 'El total no puede ser negativo'})
        
        if paid_amount < 0:
            raise serializers.ValidationError({'paid_amount': 'El monto pagado no puede ser negativo'})
        
        if paid_amount > total:
            raise serializers.ValidationError({'paid_amount': 'El monto pagado no puede exceder el total'})
        
        return data
    
    def validate_contract_relationship(self, data):
        """Validar relación con contrato"""
        document_type = data.get('document_type')
        contract = data.get('contract')
        
        if document_type == 'contrato' and not contract:
            raise serializers.ValidationError({
                'contract': 'Debe seleccionar un contrato para pedidos de tipo contrato'
            })
        
        if document_type != 'contrato' and contract:
            raise serializers.ValidationError({
                'contract': 'Solo los pedidos de tipo contrato pueden tener un contrato relacionado'
            })
        
        return data
    
    def validate_client_consistency(self, data):
        """Validar consistencia entre tipo de cliente y datos del cliente"""
        client_type = data.get('client_type')
        school_level = data.get('school_level')
        grade = data.get('grade')
        section = data.get('section')
        
        if client_type == 'colegio':
            if not school_level:
                raise serializers.ValidationError({
                    'school_level': 'El nivel es obligatorio para colegios'
                })
        
        return data
    
    def validate_scheduled_dates(self, data):
        """Validar fechas programadas"""
        scheduled_dates = data.get('scheduled_dates', {})
        
        if scheduled_dates:
            # Validar estructura de sesiones fotográficas
            if 'sesiones_fotograficas' in scheduled_dates:
                sessions = scheduled_dates['sesiones_fotograficas']
                if not isinstance(sessions, list):
                    raise serializers.ValidationError({
                        'scheduled_dates': 'Las sesiones fotográficas deben ser una lista'
                    })
                
                for i, session in enumerate(sessions):
                    if not isinstance(session, dict):
                        raise serializers.ValidationError({
                            'scheduled_dates': f'La sesión {i+1} debe ser un objeto'
                        })
                    
                    if 'fecha' not in session or 'hora' not in session:
                        raise serializers.ValidationError({
                            'scheduled_dates': f'La sesión {i+1} debe tener fecha y hora'
                        })
            
            # Validar estructura de entregas
            if 'entregas' in scheduled_dates:
                deliveries = scheduled_dates['entregas']
                if not isinstance(deliveries, list):
                    raise serializers.ValidationError({
                        'scheduled_dates': 'Las entregas deben ser una lista'
                    })
                
                for i, delivery in enumerate(deliveries):
                    if not isinstance(delivery, dict):
                        raise serializers.ValidationError({
                            'scheduled_dates': f'La entrega {i+1} debe ser un objeto'
                        })
                    
                    if 'fecha' not in delivery or 'hora' not in delivery:
                        raise serializers.ValidationError({
                            'scheduled_dates': f'La entrega {i+1} debe tener fecha y hora'
                        })
        
        return data
    
    def validate(self, data):
        """Validación general"""
        # Validar fechas
        data = self.validate_dates(data)
        
        # Validar montos
        data = self.validate_amounts(data)
        
        # Validar relación con contrato
        data = self.validate_contract_relationship(data)
        
        # Validar consistencia del cliente
        data = self.validate_client_consistency(data)
        
        # Validar fechas programadas
        data = self.validate_scheduled_dates(data)
        
        return data
    
    def create(self, validated_data):
        """Crear pedido con items"""
        items_data = validated_data.pop('items', [])
        
        # Crear el pedido
        order = Order.objects.create(**validated_data)
        
        # Crear items si se proporcionan
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        # Actualizar totales del pedido
        order.save()
        
        return order
    
    def update(self, instance, validated_data):
        """Actualizar pedido con items"""
        items_data = validated_data.pop('items', None)
        
        # Actualizar campos del pedido
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        # Actualizar items si se proporcionan
        if items_data is not None:
            # Eliminar items existentes y crear nuevos
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
        
        # Recalcular totales
        instance.save()
        
        return instance


class OrderSummarySerializer(serializers.Serializer):
    """Serializador para resumen de pedidos"""
    total_orders = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_paid = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_balance = serializers.DecimalField(max_digits=15, decimal_places=2)
    
    # Contadores por estado
    pending_orders = serializers.IntegerField()
    in_process_orders = serializers.IntegerField()
    completed_orders = serializers.IntegerField()
    delayed_orders = serializers.IntegerField()
    cancelled_orders = serializers.IntegerField()
    
    # Contadores por tipo de documento
    proforma_orders = serializers.IntegerField()
    sale_note_orders = serializers.IntegerField()
    contract_orders = serializers.IntegerField()


class ClientAutocompleteSerializer(serializers.ModelSerializer):
    """Serializador para autocompletado de clientes"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'dni', 'address', 'client_type']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class ProductSerializer(serializers.ModelSerializer):
    """Serializador para productos/servicios"""
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'product_type', 'unit_price', 'cost_price', 'stock_quantity', 'is_active']
        read_only_fields = ['id']
    
    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio unitario no puede ser negativo")
        return value
    
    def validate_cost_price(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio de costo no puede ser negativo")
        return value
    
    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value
    
    def validate_min_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock mínimo no puede ser negativo")
        return value