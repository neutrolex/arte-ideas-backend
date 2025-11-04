from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    dni = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ruc = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tenant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Cliente
        fields = '__all__'

    def validate(self, attrs):
        tipo = attrs.get('tipo_cliente')
        dni = attrs.get('dni')
        ruc = attrs.get('ruc')
        telefono = attrs.get('telefono_contacto')

        if not telefono:
            raise serializers.ValidationError({'telefono_contacto': 'El teléfono es obligatorio'})

        if tipo == 'particular':
            if not dni or not str(dni).isdigit() or len(str(dni)) != 8:
                raise serializers.ValidationError({'dni': 'El DNI es obligatorio y debe tener 8 dígitos'})
            attrs['ruc'] = None
        else:
            if not ruc or not str(ruc).isdigit() or len(str(ruc)) != 11:
                raise serializers.ValidationError({'ruc': 'El RUC es obligatorio y debe tener 11 dígitos'})
            attrs['dni'] = None
        return attrs