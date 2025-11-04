from rest_framework import serializers

from .models import Contract
from apps.crm.clientes.models import Cliente


class ContractSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Contract
        fields = (
            'id', 'tenant', 'client', 'client_name', 'title', 'contract_type',
            'status', 'amount', 'start_date', 'end_date', 'details',
            'document', 'external_ref'
        )
        read_only_fields = ('tenant', 'document')

    def validate(self, attrs):
        start_date = attrs.get('start_date', getattr(self.instance, 'start_date', None))
        end_date = attrs.get('end_date', getattr(self.instance, 'end_date', None))
        amount = attrs.get('amount', getattr(self.instance, 'amount', None))
        client = attrs.get('client', getattr(self.instance, 'client', None))
        client_name = attrs.get('client_name', getattr(self.instance, 'client_name', None))

        errors = {}
        if end_date and start_date and end_date < start_date:
            errors['end_date'] = 'La fecha de fin no puede ser menor que la de inicio'
        if amount is None or amount < 0:
            errors['amount'] = 'El monto debe ser 0 o mayor'
        if not client and not client_name:
            errors['client'] = 'Debe especificarse un cliente (FK) o client_name'

        if errors:
            raise serializers.ValidationError(errors)
        return attrs