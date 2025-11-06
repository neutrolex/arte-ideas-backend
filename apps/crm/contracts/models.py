from django.db import models
from django.core.exceptions import ValidationError

from apps.core.models import Tenant


TIPOS_CONTRATO = [
    ("FOTOGRAFIA", "Servicio Fotografía"),
    ("ENMARCADO", "Enmarcado"),
    ("GRADUACIONES", "Graduaciones"),
    ("LASER", "Corte Láser"),
    ("EVENTO", "Evento"),
    ("PERSONALIZADO", "Personalizado"),
]

ESTADOS_CONTRATO = [
    ("BORRADOR", "Borrador"),
    ("PENDIENTE", "Pendiente Aprobación"),
    ("ACTIVO", "Activo"),
    ("SUSPENDIDO", "Suspendido"),
    ("COMPLETADO", "Completado"),
    ("CANCELADO", "Cancelado"),
]


class Contrato(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.PROTECT, db_index=True, related_name="contratos_crm"
    )
    cliente = models.ForeignKey(
        "crm.Cliente",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="contratos_crm",
    )
    nombre_cliente = models.CharField(max_length=120, blank=True)

    titulo = models.CharField(max_length=160)
    tipo_contrato = models.CharField(max_length=15, choices=TIPOS_CONTRATO)
    estado = models.CharField(
        max_length=12, choices=ESTADOS_CONTRATO, default="BORRADOR", db_index=True
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    detalles = models.TextField(blank=True)
    documento = models.FileField(upload_to="contratos/", blank=True)
    referencia_externa = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = "crm_contratos"
        indexes = [
            models.Index(fields=["tenant", "estado"]),
            models.Index(fields=["tenant", "tipo_contrato"]),
        ]
        ordering = ["-fecha_inicio"]
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"

    def clean(self):
        errors = {}
        if self.fecha_fin and self.fecha_inicio and self.fecha_fin < self.fecha_inicio:
            errors["fecha_fin"] = "La fecha de fin no puede ser menor que la de inicio"
        if self.monto is None or self.monto < 0:
            errors["monto"] = "El monto debe ser 0 o mayor"
        if not self.cliente and not self.nombre_cliente:
            errors["cliente"] = "Debe especificarse un cliente (FK) o nombre_cliente"
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.titulo} ({self.estado})"