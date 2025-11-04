from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Contract
from .serializers import ContractSerializer
from .services import ContractPDFService


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, "tenant") and user.tenant:
            return self.queryset.filter(tenant=user.tenant)
        elif user.is_superuser:
            return self.queryset.all()
        return Contract.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated and hasattr(user, "tenant") and user.tenant:
            serializer.save(tenant=user.tenant)
        else:
            # Por ahora, no se guarda si no hay un tenant claro
            pass

    @action(detail=True, methods=["get"], url_path="download")
    def download(self, request, pk=None):
        contract = self.get_object()
        try:
            service = ContractPDFService(contract.tenant, request.user)
            filename = service.generate_contract(contract)
        except RuntimeError as e:
            return Response({"detail": str(e)}, status=status.HTTP_501_NOT_IMPLEMENTED)
        # Responder con información del archivo generado
        return Response(
            {
                "filename": filename,
                "document": contract.document.url if contract.document else None,
            }
        )