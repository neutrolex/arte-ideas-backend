from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Contrato
from .serializers import ContratoSerializer
from .services import ContractPDFService, PDFNotImplemented


class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_superuser', False):
            return Contrato.objects.all()
        return Contrato.objects.filter(tenant=user.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

    @action(detail=True, methods=['post'], url_path='descargar')
    def descargar(self, request, pk=None):
        contrato = self.get_object()
        try:
            ContractPDFService.generate(contrato)
        except PDFNotImplemented:
            return Response({'detail': 'PDF no disponible (dependencia no instalada)'}, status=status.HTTP_501_NOT_IMPLEMENTED)
        return Response({'detail': 'PDF generado', 'documento': contrato.documento.url if contrato.documento else None})