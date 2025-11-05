from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import Tenant


def validar_ruc(value):
    if value and not value.isdigit() or (value and len(value) != 11):
        raise ValidationError('El RUC debe tener 11 dígitos numéricos')


def validar_dni(value):
    if value and not value.isdigit() or (value and len(value) != 8):
        raise ValidationError('El DNI debe tener 8 dígitos numéricos')


class Cliente(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    TIPO_CLIENTE_CHOICES = [
        ('particular', 'Particular'),
        ('colegio', 'Colegio'),
        ('empresa', 'Empresa'),
    ]

    nombre_completo = models.CharField(max_length=150)
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE_CHOICES, default='particular')
    dni = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[validar_dni],
        help_text='Requerido para clientes particulares (8 dígitos)'
    )
    ruc = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[validar_ruc],
        help_text='Requerido para empresas y colegios (11 dígitos)'
    )
    telefono_contacto = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    institucion_educativa = models.CharField(max_length=150, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    detalles_adicionales = models.TextField(blank=True, null=True)

    pedidos = models.PositiveIntegerField(default=0)
    total_gastado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ultima_fecha_pedido = models.DateField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'dni'],
                name='unique_tenant_dni_when_not_null',
                condition=models.Q(dni__isnull=False) & ~models.Q(dni='')
            ),
            models.UniqueConstraint(
                fields=['tenant', 'ruc'],
                name='unique_tenant_ruc_when_not_null',
                condition=models.Q(ruc__isnull=False) & ~models.Q(ruc='')
            ),
        ]

    def clean(self):
        # Validación de tipo de cliente
        if self.tipo_cliente == 'particular':
            if not self.dni:
                raise ValidationError({'dni': 'El DNI es obligatorio para clientes particulares'})
            self.ruc = None  # Limpiar RUC si es particular
        else:
            if not self.ruc:
                raise ValidationError({'ruc': 'El RUC es obligatorio para empresas y colegios'})
            self.dni = None  # Limpiar DNI si es empresa o colegio

        # Validación de unicidad para DNI por tenant (solo si no es nulo o vacío)
        if self.dni and self.dni.strip():
            qs = Cliente.objects.filter(tenant=self.tenant, dni=self.dni)
            if self.pk:  # Si el objeto ya existe, lo excluimos de la consulta
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({'dni': 'Ya existe un cliente registrado con este DNI.'})

        # Validación de unicidad para RUC por tenant (solo si no es nulo o vacío)
        if self.ruc and self.ruc.strip():
            qs = Cliente.objects.filter(tenant=self.tenant, ruc=self.ruc)
            if self.pk:  # Si el objeto ya existe, lo excluimos de la consulta
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({'ruc': 'Ya existe un cliente registrado con este RUC.'})

    def __str__(self):
        return self.nombre_completo