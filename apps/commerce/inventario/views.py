from django.db.models import Sum, Count, Q, F
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    MolduraListon, MolduraPrearmada, VidrioTapaMDF, Paspartu,
    Minilab, Cuadro, Anuario, CorteLaser, MarcoAccesorio, HerramientaGeneral
)
from .serializers import (
    MolduraListonSerializer, MolduraPrearmadaSerializer, VidrioTapaMDFSerializer,
    PaspartuSerializer, MinilabSerializer, CuadroSerializer, AnuarioSerializer,
    CorteLaserSerializer, MarcoAccesorioSerializer, HerramientaGeneralSerializer
)


@api_view(['GET'])
def dashboard_inventario(request):
    """API endpoint para obtener métricas principales del inventario"""
    
    # Obtener todos los modelos de inventario
    modelos_inventario = [
        MolduraListon, MolduraPrearmada, VidrioTapaMDF, Paspartu,
        Minilab, Cuadro, Anuario, CorteLaser, MarcoAccesorio, HerramientaGeneral
    ]
    
    # Calcular métricas principales
    total_productos = 0
    stock_total = 0
    alertas_stock = 0
    valor_total_inventario = 0
    
    for modelo in modelos_inventario:
        productos = modelo.objects.all()
        total_productos += productos.count()
        stock_total += productos.aggregate(Sum('stock_disponible'))['stock_disponible__sum'] or 0
        alertas_stock += productos.filter(stock_disponible__lte=F('stock_minimo')).count()
        
        # Calcular valor total del inventario
        for producto in productos:
            valor_total_inventario += float(producto.costo_total)
    
    # Productos con alertas de stock
    productos_alerta = []
    for modelo in modelos_inventario:
        alertas = modelo.objects.filter(stock_disponible__lte=F('stock_minimo'))
        for producto in alertas:
            productos_alerta.append({
                'categoria': modelo._meta.verbose_name,
                'nombre': producto.nombre_producto,
                'stock_actual': producto.stock_disponible,
                'stock_minimo': producto.stock_minimo,
            })
    
    data = {
        'total_productos': total_productos,
        'stock_total': stock_total,
        'alertas_stock': alertas_stock,
        'valor_total_inventario': valor_total_inventario,
        'productos_alerta': productos_alerta,
    }
    
    return Response(data)


@api_view(['GET'])
def metricas_api(request):
    """API endpoint para obtener métricas del inventario en formato JSON"""
    
    modelos_inventario = [
        MolduraListon, MolduraPrearmada, VidrioTapaMDF, Paspartu,
        Minilab, Cuadro, Anuario, CorteLaser, MarcoAccesorio, HerramientaGeneral
    ]
    
    metricas = {
        'total_productos': 0,
        'stock_total': 0,
        'alertas_stock': 0,
        'valor_total_inventario': 0,
        'categorias': {}
    }
    
    for modelo in modelos_inventario:
        productos = modelo.objects.all()
        categoria = modelo._meta.verbose_name_plural
        
        count = productos.count()
        stock = productos.aggregate(Sum('stock_disponible'))['stock_disponible__sum'] or 0
        alertas = productos.filter(stock_disponible__lte=F('stock_minimo')).count()
        
        metricas['total_productos'] += count
        metricas['stock_total'] += stock
        metricas['alertas_stock'] += alertas
        
        # Calcular valor por categoría
        valor_categoria = sum(p.costo_total for p in productos)
        metricas['valor_total_inventario'] += valor_categoria
        
        metricas['categorias'][categoria] = {
            'productos': count,
            'stock': stock,
            'alertas': alertas,
            'valor': float(valor_categoria)
        }
    
    return Response(metricas)

# ViewSets para API REST completa
class BaseInventarioViewSet(viewsets.ModelViewSet):
    """ViewSet base para todos los modelos de inventario"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def alertas_stock(self, request):
        """Endpoint para obtener productos con alertas de stock"""
        productos_alerta = self.get_queryset().filter(stock_disponible__lte=F('stock_minimo'))
        serializer = self.get_serializer(productos_alerta, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        """Endpoint para obtener productos con stock bajo (menos del 20% del stock mínimo)"""
        productos_bajo_stock = self.get_queryset().filter(
            stock_disponible__lte=F('stock_minimo') * 0.2
        )
        serializer = self.get_serializer(productos_bajo_stock, many=True)
        return Response(serializer.data)


class MolduraListonViewSet(BaseInventarioViewSet):
    queryset = MolduraListon.objects.all()
    serializer_class = MolduraListonSerializer


class MolduraPrearmadaViewSet(BaseInventarioViewSet):
    queryset = MolduraPrearmada.objects.all()
    serializer_class = MolduraPrearmadaSerializer


class VidrioTapaMDFViewSet(BaseInventarioViewSet):
    queryset = VidrioTapaMDF.objects.all()
    serializer_class = VidrioTapaMDFSerializer


class PaspartuViewSet(BaseInventarioViewSet):
    queryset = Paspartu.objects.all()
    serializer_class = PaspartuSerializer


class MinilabViewSet(BaseInventarioViewSet):
    queryset = Minilab.objects.all()
    serializer_class = MinilabSerializer


class CuadroViewSet(BaseInventarioViewSet):
    queryset = Cuadro.objects.all()
    serializer_class = CuadroSerializer


class AnuarioViewSet(BaseInventarioViewSet):
    queryset = Anuario.objects.all()
    serializer_class = AnuarioSerializer


class CorteLaserViewSet(BaseInventarioViewSet):
    queryset = CorteLaser.objects.all()
    serializer_class = CorteLaserSerializer


class MarcoAccesorioViewSet(BaseInventarioViewSet):
    queryset = MarcoAccesorio.objects.all()
    serializer_class = MarcoAccesorioSerializer


class HerramientaGeneralViewSet(BaseInventarioViewSet):
    queryset = HerramientaGeneral.objects.all()
    serializer_class = HerramientaGeneralSerializer