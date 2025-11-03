"""
Views del Core App - Arte Ideas
Solo contiene vistas compartidas entre módulos
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class CoreHealthCheckView(APIView):
    """Vista de health check para el Core App"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Health check del sistema"""
        return Response({
            'status': 'ok',
            'message': 'Arte Ideas Core App funcionando correctamente',
            'modules': {
                'profile': 'Mi Perfil - Gestión personal del usuario',
                'configuration': 'Configuración - Gestión de usuarios, negocio y permisos'
            }
        })