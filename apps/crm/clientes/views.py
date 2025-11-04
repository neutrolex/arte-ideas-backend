from rest_framework import viewsets
from .models import Cliente
from .serializers import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'tenant') and user.tenant:
            return self.queryset.filter(tenant=user.tenant)
        elif getattr(user, 'is_superuser', False):
            return self.queryset.all()
        return Cliente.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'tenant') and user.tenant:
            serializer.save(tenant=user.tenant)
        else:
            # Manejar caso de superuser o asignar un tenant por defecto si es necesario
            # Por ahora, no se guarda si no hay un tenant claro.
            pass