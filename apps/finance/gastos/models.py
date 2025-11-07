from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel

from apps.core.models.user import User
from apps.core.managers import TenantManager


# --- Choices Fields ---
class EstadosGastoPersonal(models.TextChoices):
    PENDIENTE = 'Pendiente', _('Pendiente')
    PAGADO = 'Pagado', _('Pagado')

class EstadosGastoServicio(models.TextChoices):
    PENDIENTE = 'Pendiente', _('Pendiente')
    PAGADO = 'Pagado', _('Pagado')
    VENCIDO = 'Vencido', _('Vencido')

class TiposGastoServicio(models.TextChoices):
    ALQUILER = 'Alquiler', _('Alquiler')
    LUZ = 'Luz', _('Luz')
    AGUA = 'Agua', _('Agua')
    INTERNET = 'Internet', _('Internet')
    TELEFONO = 'Teléfono', _('Teléfono')
    GAS = 'Gas', _('Gas')
    OTRO = 'Otro', _('Otro') 

class MetodosPago(models.TextChoices):
    EFECTIVO = 'Efectivo', _('Efectivo')
    TRANSFERENCIA = 'Transferencia', _('Transferencia')
    TARJETA = 'Tarjeta', _('Tarjeta')
    DEPOSITO = 'Deposito', _('Depósito')
    OTRO = 'Otro', _('Otro')


# --- ExpenseCategory Model (Modelo simple) ---
class ExpenseCategory(BaseModel):
    
    nombre = models.CharField(_("nombre de categoría"), max_length=100)
    descripcion = models.TextField(_("descripción"), blank=True)
    is_active = models.BooleanField(_("está activo"), default=True)

    objects = TenantManager()

    class Meta:
        verbose_name = _("categoría de gasto")
        verbose_name_plural = _("categorías de gasto")
        unique_together = ['tenant', 'nombre']

    def __str__(self):
        return self.nombre


# --- PersonalExpense Model ---
class PersonalExpense(BaseModel):

    codigo = models.CharField(_("código"), max_length=20)
    nombre = models.CharField(_("nombre completo"), max_length=100)
    cargo = models.CharField(_("cargo"), max_length=50)
    salario_base = models.DecimalField(_("salario base"), max_digits=10, decimal_places=2)
    bonificaciones = models.DecimalField(_("bonificaciones"), max_digits=10, decimal_places=2, default=0)
    descuentos = models.DecimalField(_("descuentos"), max_digits=10, decimal_places=2, default=0)
    fecha_pago = models.DateField(_("fecha de pago"), null=True, blank=True)
    estado = models.CharField(
        _("estado"),
        max_length=20,
        choices=EstadosGastoPersonal.choices,
        default=EstadosGastoPersonal.PENDIENTE
    )
    
    categoria = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="personal_expenses"
    )

    
    objects = TenantManager()

    @property
    def salario_neto(self):
        return (self.salario_base + self.bonificaciones) - self.descuentos

    class Meta:
        verbose_name = _("gasto de personal")
        verbose_name_plural = _("gastos de personal")
        ordering = ['-created_at']
        unique_together = ['tenant', 'codigo']

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


# --- ServiceExpense Model ---
class ServiceExpense(BaseModel):
    
    codigo = models.CharField(_("código"), max_length=20)
    tipo = models.CharField(
        _("tipo de servicio"),
        max_length=50,
        choices=TiposGastoServicio.choices
    )
    proveedor = models.CharField(_("proveedor"), max_length=100)
    monto = models.DecimalField(_("monto"), max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField(_("fecha de vencimiento"))
    fecha_pago = models.DateField(_("fecha de pago"), null=True, blank=True)
    periodo = models.CharField(_("periodo"), max_length=50, help_text=_("Ej: Enero 2025"))
    estado = models.CharField(
        _("estado"),
        max_length=20,
        choices=EstadosGastoServicio.choices,
        default=EstadosGastoServicio.PENDIENTE
    )


    categoria = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="service_expenses"
    )


    objects = TenantManager()

    class Meta:
        verbose_name = _("gasto de servicio")
        verbose_name_plural = _("gastos de servicio")
        ordering = ['-fecha_vencimiento']
        unique_together = ['tenant', 'codigo']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.proveedor} ({self.periodo})"


# --- Budget Model ---
class Budget(BaseModel):

    categoria = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.CASCADE,
        related_name="budgets"
    )
    periodo_inicio = models.DateField(_("inicio del periodo"))
    periodo_fin = models.DateField(_("fin del periodo"))
    monto_presupuestado = models.DecimalField(_("monto presupuestado"), max_digits=12, decimal_places=2)
    monto_gastado = models.DecimalField(_("monto gastado"), max_digits=12, decimal_places=2, default=0)

    objects = TenantManager()

    @property
    def balance(self):
        return self.monto_presupuestado - self.monto_gastado
    
    @property
    def porcentaje_gastado(self):
        if self.monto_presupuestado == 0:
            return 0
        return (self.monto_gastado / self.monto_presupuestado) * 100

    class Meta:
        verbose_name = _("presupuesto")
        verbose_name_plural = _("presupuestos")
        unique_together = ['tenant', 'categoria', 'periodo_inicio', 'periodo_fin']

    def __str__(self):
        return f"{self.categoria.nombre} ({self.periodo_inicio} - {self.periodo_fin})"