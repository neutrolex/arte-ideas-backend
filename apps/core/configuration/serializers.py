"""
Serializers del Módulo Configuración - Arte Ideas
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from apps.core.models import Tenant, TenantConfiguration, RolePermission, UserProfile

User = get_user_model()


class TenantSerializer(serializers.ModelSerializer):
    """Serializer para datos del tenant"""
    location_display = serializers.CharField(source='get_location_type_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    
    class Meta:
        model = Tenant
        fields = [
            'id', 'name', 'slug', 'business_name', 'business_address',
            'business_phone', 'business_email', 'business_ruc', 'currency',
            'currency_display', 'location_type', 'location_display',
            'max_users', 'is_active'
        ]
        read_only_fields = ['id', 'slug']


class TenantConfigurationSerializer(serializers.ModelSerializer):
    """Serializer para configuraciones del tenant"""
    typed_value = serializers.SerializerMethodField()
    
    class Meta:
        model = TenantConfiguration
        fields = ['module', 'key', 'value', 'typed_value', 'data_type', 'description', 'is_editable']
    
    def get_typed_value(self, obj):
        return obj.get_typed_value()


class RolePermissionSerializer(serializers.ModelSerializer):
    """Serializer para permisos por rol"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    modules_count = serializers.SerializerMethodField()
    sensitive_actions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = RolePermission
        fields = [
            'role', 'role_display', 'modules_count', 'sensitive_actions_count',
            # Módulos
            'access_dashboard', 'access_agenda', 'access_pedidos', 'access_clientes',
            'access_inventario', 'access_activos', 'access_gastos', 'access_produccion',
            'access_contratos', 'access_reportes',
            # Acciones sensibles
            'view_costos', 'view_precios', 'view_margenes', 'view_datos_clientes',
            'view_datos_financieros', 'edit_precios', 'delete_registros'
        ]
    
    def get_modules_count(self, obj):
        """Contar módulos con acceso"""
        modules = [
            obj.access_dashboard, obj.access_agenda, obj.access_pedidos,
            obj.access_clientes, obj.access_inventario, obj.access_activos,
            obj.access_gastos, obj.access_produccion, obj.access_contratos,
            obj.access_reportes
        ]
        return sum(modules)
    
    def get_sensitive_actions_count(self, obj):
        """Contar acciones sensibles permitidas"""
        actions = [
            obj.view_costos, obj.view_precios, obj.view_margenes,
            obj.view_datos_clientes, obj.view_datos_financieros,
            obj.edit_precios, obj.delete_registros
        ]
        return sum(actions)


class UserManagementSerializer(serializers.ModelSerializer):
    """Serializer para gestión de usuarios en configuración"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'is_active', 'status_display',
            'phone', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_status_display(self, obj):
        return "Activo" if obj.is_active else "Inactivo"


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer para crear nuevos usuarios"""
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'password', 'confirm_password'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return attrs
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        
        # Asignar tenant del usuario actual
        tenant = self.context['request'].user.tenant
        validated_data['tenant'] = tenant
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        # Crear perfil
        UserProfile.objects.create(user=user)
        
        return user


class SuperAdminTenantSerializer(serializers.ModelSerializer):
    """Serializer para gestión de tenants (solo super admin)"""
    users_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tenant
        fields = [
            'id', 'name', 'slug', 'business_name', 'business_email',
            'location_type', 'currency', 'max_users', 'users_count',
            'is_active', 'created_at'
        ]
    
    def get_users_count(self, obj):
        return obj.user_set.count()