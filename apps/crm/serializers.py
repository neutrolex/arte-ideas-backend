"""
Serializers del CRM App - Arte Ideas
"""
from rest_framework import serializers
from .models import Cliente, Contrato


class ClienteSerializer(serializers.ModelSerializer):
    dni = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ruc = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant = serializers.PrimaryKeyRelatedField(read_only=True)
    nombre_completo = serializers.ReadOnlyField(source='obtener_nombre_completo')

    class Meta:
        model = Cliente
        fields = '__all__'

    def validate(self, attrs):
        tipo = attrs.get('tipo_cliente')
        dni = attrs.get('dni')
        ruc = attrs.get('ruc')
        telefono = attrs.get('telefono')

        if not telefono:
            raise serializers.ValidationError({'telefono': 'El teléfono es obligatorio'})

        if tipo == 'particular':
            if not dni or not str(dni).isdigit() or len(str(dni)) != 8:
                raise serializers.ValidationError({'dni': 'El DNI es obligatorio y debe tener 8 dígitos'})
            attrs['ruc'] = None
        else:
            if not ruc or not str(ruc).isdigit() or len(str(ruc)) != 11:
                raise serializers.ValidationError({'ruc': 'El RUC es obligatorio y debe tener 11 dígitos'})
            attrs['dni'] = None
        return attrs


class ContratoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.ReadOnlyField(source='cliente.obtener_nombre_completo')
    tenant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Contrato
        fields = '__all__'

    def validate(self, attrs):
        fecha_inicio = attrs.get('fecha_inicio')
        fecha_fin = attrs.get('fecha_fin')
        
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise serializers.ValidationError({
                'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio'
            })
        
        return attrs