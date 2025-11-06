from rest_framework import serializers
from .models import OrdenProduccion
from apps.core.models import User, Tenant
from apps.crm.models import Client
from apps.commerce.models import Order

class OrdenProduccionSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.ReadOnlyField(source='cliente.get_full_name')
    operario_nombre = serializers.ReadOnlyField(source='operario.get_full_name')
    pedido_codigo = serializers.ReadOnlyField(source='pedido.order_number')
    
    class Meta:
        model = OrdenProduccion
        fields = [
            'id', 'numero_op', 'pedido', 'pedido_codigo', 'cliente', 'cliente_nombre', 
            'descripcion', 'tipo', 'estado', 'prioridad', 'operario', 
            'operario_nombre', 'fecha_estimada', 'id_inquilino',
            'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en', 'id_inquilino', 'cliente']  # cliente se autocompleta
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        user_inquilino = self.context.get('user_inquilino')
        
        # Filtrar campos relacionados por inquilino
        if user_inquilino:
            # Solo pedidos del mismo inquilino
            self.fields['pedido'].queryset = Order.objects.filter(tenant=user_inquilino)
            # Solo operarios del mismo inquilino
            self.fields['operario'].queryset = User.objects.filter(
                role='operario',
                tenant=user_inquilino
            )
        
        # Ocultar id_inquilino para usuarios no superusuarios
        if request and hasattr(request, 'user'):
            if not request.user.is_superuser:
                # Remover id_inquilino de los campos visibles
                if 'id_inquilino' in self.fields:
                    del self.fields['id_inquilino']
    

    
    def create(self, validated_data):
        """Asignar automáticamente cliente e inquilino"""
        pedido = validated_data.get('pedido')
        request = self.context.get('request')
        
        # Autocompletar cliente según pedido
        if pedido:
            validated_data['cliente'] = pedido.client
        
        # Asignar automáticamente el inquilino del usuario
        if request and hasattr(request.user, 'tenant') and request.user.tenant:
            validated_data['id_inquilino'] = request.user.tenant
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Prevenir cambio de inquilino en actualizaciones"""
        # Remover id_inquilino de validated_data para prevenir cambios accidentales
        validated_data.pop('id_inquilino', None)
        
        # Autocompletar cliente si se cambia el pedido
        pedido = validated_data.get('pedido')
        if pedido:
            validated_data['cliente'] = pedido.client
        
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        """Personalizar la representación según el tipo de usuario"""
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        # Solo mostrar id_inquilino a superusuarios
        if request and hasattr(request, 'user'):
            if not request.user.is_superuser and 'id_inquilino' in data:
                del data['id_inquilino']
        
        return data
    
    def validate_numero_op(self, value):
        # Verificar que el número de OP sea único
        if OrdenProduccion.objects.filter(numero_op=value).exists():
            if self.instance and self.instance.numero_op == value:
                return value
            raise serializers.ValidationError("Este número de orden ya existe.")
        return value
    
    def validate_operario(self, value):
        # Verificar que el operario tenga el rol correcto
        if value and value.role != 'operario':
            raise serializers.ValidationError("El usuario seleccionado no tiene el rol de Operario.")
        return value
    
    def validate(self, data):
        # Verificar que todos los campos requeridos estén presentes
        # Nota: id_inquilino y cliente se asignan automáticamente, no son requeridos en la validación
        required_fields = ['numero_op', 'pedido', 'descripcion', 
                          'tipo', 'estado', 'prioridad', 'operario', 
                          'fecha_estimada']
        
        for field in required_fields:
            if field not in data and (not self.instance or not getattr(self.instance, field)):
                raise serializers.ValidationError({field: "Este campo es requerido."})
        
        return data