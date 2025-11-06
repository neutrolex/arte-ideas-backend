from rest_framework import permissions

class IsSameInquilino(permissions.BasePermission):
    """
    Permiso que verifica que el usuario pertenezca al mismo inquilino que el objeto
    """
    def has_object_permission(self, request, view, obj):
        # Superusuarios tienen acceso a todo
        if request.user.is_superuser:
            return True
        
        # Verificar que el usuario pertenezca al mismo inquilino que el objeto
        return obj.id_inquilino == request.user.id_inquilino

# Mantener alias para compatibilidad
IsSameInmobiliaria = IsSameInquilino