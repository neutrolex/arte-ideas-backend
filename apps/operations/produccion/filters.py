import django_filters
from django.db import models
from .models import OrdenProduccion

class OrdenProduccionFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = OrdenProduccion
        fields = {
            'estado': ['exact'],
            'tipo': ['exact'],
            'prioridad': ['exact'],
            'cliente': ['exact'],
            'fecha_estimada': ['gte', 'lte'],
        }
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(numero_op__icontains=value) |
            models.Q(pedido__codigo__icontains=value) |
            models.Q(cliente__nombre__icontains=value) |
            models.Q(descripcion__icontains=value)
        )