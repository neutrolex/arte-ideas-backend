from rest_framework import serializers
from .models import (
    MolduraListon, MolduraPrearmada, VidrioTapaMDF, Paspartu,
    Minilab, Cuadro, Anuario, CorteLaser, MarcoAccesorio, HerramientaGeneral
)


class BaseInventarioSerializer(serializers.ModelSerializer):
    """Serializer base para todos los modelos de inventario"""
    costo_total = serializers.ReadOnlyField()
    alerta_stock = serializers.ReadOnlyField()
    
    class Meta:
        fields = [
            'id', 'nombre_producto', 'stock_disponible', 'stock_minimo', 
            'costo_unitario', 'costo_total', 'alerta_stock',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'costo_total', 'alerta_stock']


class MolduraListonSerializer(BaseInventarioSerializer):
    class Meta(BaseInventarioSerializer.Meta):
        model = MolduraListon
        fields = BaseInventarioSerializer.Meta.fields + [
            'nombre_moldura', 'ancho', 'color', 'material'
        ]


class MolduraPrearmadaSerializer(BaseInventarioSerializer):
    class Meta(BaseInventarioSerializer.Meta):
        model = MolduraPrearmada
        fields = BaseInventarioSerializer.Meta.fields + [
            'dimensiones', 'color', 'material'
        ]


class VidrioTapaMDFSerializer(BaseInventarioSerializer):
    class Meta(BaseInventarioSerializer.Meta):
        model = VidrioTapaMDF
        fields = BaseInventarioSerializer.Meta.fields + [
            'tipo_material', 'tipo_vidrio', 'grosor', 'tamaño'
        ]


class PaspartuSerializer(BaseInventarioSerializer):
    class Meta(BaseInventarioSerializer.Meta):
        model = Paspartu
        fields = BaseInventarioSerializer.Meta.fields + [
            'tipo_material', 'tamaño', 'grosor', 'color'
        ]


class MinilabSerializer(BaseInventarioSerializer):
    class Meta(BaseInventarioSerializer.Meta):
        model = Minilab
        fields = BaseInventarioSerializer.Meta.fields + [
            'tipo_insumo', 'nombre_tipo', 'tamaño_presentacion', 'fecha_compra'
        ]


class CuadroSerializer(BaseInventarioSerializer):
    class Meta(BaseInventarioSerializer.Meta):
        model = Cuadro
        fields = BaseInventarioSerializer.Meta.fields + [
            'formato', 'dimensiones', 'material'
        ]


class AnuarioSerializer(BaseInventarioSerializer):
    class Meta(BaseInventarioSerializer.Meta):
        model = Anuario
        fields = BaseInventarioSerializer.Meta.fields + [
            'formato', 'paginas', 'tipo_tapa'
        ]


class CorteLaserSerializer(BaseInventarioSerializer):
    class Meta(BaseInventarioSerializer.Meta):
        model = CorteLaser
        fields = BaseInventarioSerializer.Meta.fields + [
            'producto', 'tipo', 'tamaño', 'color', 'unidad', 'proveedor'
        ]


class MarcoAccesorioSerializer(BaseInventarioSerializer):
    class Meta(BaseInventarioSerializer.Meta):
        model = MarcoAccesorio
        fields = BaseInventarioSerializer.Meta.fields + [
            'nombre_moldura', 'tipo_moldura', 'material', 'color', 'dimensiones'
        ]


class HerramientaGeneralSerializer(BaseInventarioSerializer):
    class Meta(BaseInventarioSerializer.Meta):
        model = HerramientaGeneral
        fields = BaseInventarioSerializer.Meta.fields + [
            'nombre_herramienta', 'marca', 'tipo_material'
        ]