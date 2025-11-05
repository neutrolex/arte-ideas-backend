from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Contract
from .serializers import ContractSerializer
from .services import ContractPDFService, PDFNotImplemented


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_superuser', False):
            return Contract.objects.all()
        return Contract.objects.filter(tenant=user.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

    @action(detail=True, methods=['post'], url_path='download')
    def download(self, request, pk=None):
        contract = self.get_object()
        try:
            ContractPDFService.generate(contract)
        except PDFNotImplemented:
            return Response({'detail': 'PDF no disponible (dependencia no instalada)'}, status=status.HTTP_501_NOT_IMPLEMENTED)
        return Response({'detail': 'PDF generado', 'document': contract.document.url if contract.document else None})