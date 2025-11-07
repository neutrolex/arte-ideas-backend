from .models import Tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant = None
        
        
        tenant_id = request.META.get('HTTP_X_TENANT_ID')
        if tenant_id:
            try:
                
                tenant = Tenant._default_manager.get(id=tenant_id)
            except Tenant.DoesNotExist:
                tenant = None
        
       
        if tenant is None and hasattr(request, 'user') and request.user.is_authenticated:
            tenant = request.user.tenant

        
        request.tenant = tenant
        
        response = self.get_response(request)
        return response