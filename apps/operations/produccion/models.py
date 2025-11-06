from django.db import models
from django.conf import settings
from apps.core.models import Tenant, User
from apps.crm.models import Client
from apps.commerce.models import Order

class OrdenProduccion(models.Model):
    TIPO_CHOICES = [
        ('Enmarcado', 'Enmarcado'),
        ('Minilab', 'Minilab'),
        ('Graduación', 'Graduación'),
        ('Corte Láser', 'Corte Láser'),
        ('Edición Digital', 'Edición Digital'),
        ('Otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Terminado', 'Terminado'),
        ('Entregado', 'Entregado'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('Baja', 'Baja'),
        ('Normal', 'Normal'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]
    
    numero_op = models.CharField(max_length=20, unique=True)
    pedido = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='ordenes')
    cliente = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='ordenes')
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='Normal')
    operario = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='ordenes_asignadas',
        limit_choices_to={'role': 'operario'}
    )
    fecha_estimada = models.DateField()
    id_inquilino = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='ordenes')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Autocompletar cliente según pedido seleccionado
        if self.pedido and not self.cliente_id:
            self.cliente = self.pedido.client
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero_op} - {self.estado}"
    
    class Meta:
        verbose_name = "Orden de Producción"
        verbose_name_plural = "Órdenes de Producción"
        ordering = ['-creado_en']