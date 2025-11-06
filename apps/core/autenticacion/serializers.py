"""
Serializers del Módulo de Autenticación - Arte Ideas
"""
from rest_framework import serializers


class LogoutSerializer(serializers.Serializer):
    """Serializer para logout"""
    refresh_token = serializers.CharField(required=True)
    
    def validate_refresh_token(self, value):
        """Validar que el refresh token no esté vacío"""
        if not value:
            raise serializers.ValidationError("El refresh token es requerido")
        return value