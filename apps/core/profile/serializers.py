"""
Serializers del Módulo Mi Perfil - Arte Ideas
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from apps.core.models import UserProfile, UserActivity

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil del usuario"""
    completion_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['language', 'theme', 'email_notifications', 'completion_percentage']
    
    def get_completion_percentage(self, obj):
        """Calcular porcentaje de completitud del perfil"""
        user = obj.user
        fields = [
            user.first_name, user.last_name, user.email,
            user.phone, user.address, user.bio
        ]
        completed = sum(1 for field in fields if field)
        return int((completed / len(fields)) * 100)


class UserSerializer(serializers.ModelSerializer):
    """Serializer para datos del usuario en Mi Perfil"""
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'address', 'bio', 'avatar', 'role', 'role_display',
            'tenant_name', 'email_verified', 'is_active', 'date_joined',
            'last_login', 'profile'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'last_login', 'email_verified']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class UserStatisticsSerializer(serializers.Serializer):
    """Serializer para estadísticas del usuario"""
    orders_processed = serializers.IntegerField(default=0)
    clients_attended = serializers.IntegerField(default=0)
    sessions_completed = serializers.IntegerField(default=0)
    hours_worked = serializers.IntegerField(default=0)


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer para actividad del usuario"""
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = UserActivity
        fields = ['action', 'action_display', 'description', 'module', 'created_at', 'time_ago']
    
    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff < timedelta(minutes=1):
            return "Hace unos segundos"
        elif diff < timedelta(hours=1):
            return f"Hace {diff.seconds // 60} minutos"
        elif diff < timedelta(days=1):
            return f"Hace {diff.seconds // 3600} horas"
        else:
            return f"Hace {diff.days} días"


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambio de contraseña"""
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return attrs


class ChangeEmailSerializer(serializers.Serializer):
    """Serializer para cambio de email"""
    new_email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña es incorrecta.")
        return value
    
    def validate_new_email(self, value):
        user = self.context['request'].user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Este email ya está en uso.")
        return value