from rest_framework.permissions import BasePermission

class TenantPermission(BasePermission):
    

    def has_permission(self, request, view):
       
        if not request.user or not request.user.is_authenticated or not request.user.tenant:
            return False
        
       
        if not hasattr(request, 'tenant'):
            
            return False

        
        return request.user.tenant == request.tenant
    
    def has_object_permission(self, request, view, obj):
        
        if not hasattr(obj, 'tenant'):
            
            return False
            
        return obj.tenant == request.user.tenant