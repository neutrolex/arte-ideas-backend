from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrdenProduccionViewSet

# Configuración del router para las vistas basadas en ViewSet
router = DefaultRouter()
router.register(r'produccion/ordenes', OrdenProduccionViewSet, basename='orden-produccion')

# Lista de endpoints disponibles:
# GET /api/produccion/ordenes/ - Listar todas las órdenes de producción
# POST /api/produccion/ordenes/ - Crear una nueva orden de producción
# GET /api/produccion/ordenes/{id}/ - Obtener detalles de una orden específica
# PUT /api/produccion/ordenes/{id}/ - Actualizar una orden completa
# PATCH /api/produccion/ordenes/{id}/ - Actualizar parcialmente una orden
# DELETE /api/produccion/ordenes/{id}/ - Eliminar una orden
# GET /api/produccion/ordenes/dashboard/ - Obtener estadísticas del dashboard

urlpatterns = [
    # Incluir todas las rutas generadas por el router
    path('', include(router.urls)),
    
    # Rutas adicionales pueden ser agregadas aquí si es necesario
]