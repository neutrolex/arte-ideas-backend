from rest_framework import serializers

from .models import Contrato
from apps.crm.models import Cliente


class ContratoSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), required=False, allow_null=True
    )
    cliente_nombre = serializers.ReadOnlyField(source='cliente.obtener_nombre_completo')

    class Meta:
        model = Contrato
        fields = (
            'id', 'tenant', 'cliente', 'cliente_nombre', 'nombre_cliente', 'titulo', 'tipo_contrato',
            'estado', 'monto', 'fecha_inicio', 'fecha_fin', 'detalles',
            'documento', 'referencia_externa'
        )
        read_only_fields = ('tenant', 'documento')

    def validate(self, attrs):
        fecha_inicio = attrs.get('fecha_inicio', getattr(self.instance, 'fecha_inicio', None))
        fecha_fin = attrs.get('fecha_fin', getattr(self.instance, 'fecha_fin', None))
        monto = attrs.get('monto', getattr(self.instance, 'monto', None))
        cliente = attrs.get('cliente', getattr(self.instance, 'cliente', None))
        nombre_cliente = attrs.get('nombre_cliente', getattr(self.instance, 'nombre_cliente', None))

        errors = {}
        if fecha_fin and fecha_inicio and fecha_fin < fecha_inicio:
            errors['fecha_fin'] = 'La fecha de fin no puede ser menor que la de inicio'
        if monto is None or monto < 0:
            errors['monto'] = 'El monto debe ser 0 o mayor'
        if not cliente and not nombre_cliente:
            errors['cliente'] = 'Debe especificarse un cliente (FK) o nombre_cliente'

        if errors:
            raise serializers.ValidationError(errors)
        return attrs