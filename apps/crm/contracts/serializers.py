from rest_framework import serializers

from .models import Contract
from apps.crm.clientes.models import Cliente


class ContractSerializer(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(read_only=True)
    client = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Cliente.objects.all())

    class Meta:
        model = Contract
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        # Validaciones adicionales simples
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        amount = attrs.get("amount")
        client = attrs.get("client")
        client_name = attrs.get("client_name")

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "La fecha de fin no puede ser menor que la de inicio"})
        if amount is None or amount < 0:
            raise serializers.ValidationError({"amount": "El monto debe ser 0 o mayor"})
        if not client and not client_name:
            raise serializers.ValidationError({"client": "Debe especificarse un cliente (FK) o client_name"})
        return attrs