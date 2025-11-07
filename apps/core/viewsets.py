from rest_framework import viewsets, permissions
from .permissions import TenantPermission 

class TenantViewSet(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated, TenantPermission]

    def get_queryset(self):
        
        return self.queryset.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        
        serializer.save(
            tenant=self.request.user.tenant, 
            created_by=self.request.user
        )

    def perform_update(self, serializer):
      
        serializer.save(updated_by=self.request.user)