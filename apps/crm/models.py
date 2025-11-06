"""
Modelos del CRM App - Arte Ideas
Gestión de clientes y relaciones comerciales
"""
from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import Tenant


class Cliente(models.Model):
    """
    Modelo para clientes del estudio fotográfico
    Soporta diferentes tipos de clientes: Particular, Colegio, Empresa
    """
    TIPO_CLIENTE_CHOICES = [
        ('particular', 'Particular'),
        ('colegio', 'Colegio'),
        ('empresa', 'Empresa'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Estudio Fotográfico')
    
    # Información básica del cliente
    tipo_cliente = models.CharField(
        max_length=20, 
        choices=TIPO_CLIENTE_CHOICES, 
        default='particular',
        verbose_name='Tipo de Cliente'
    )
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    email = models.EmailField(verbose_name='Email')
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    dni = models.CharField(max_length=15, verbose_name='DNI/RUC', unique=True)
    direccion = models.TextField(verbose_name='Dirección')
    
    # Campos específicos para colegios
    nivel_educativo = models.CharField(
        max_length=20,
        choices=[
            ('inicial', 'Inicial'),
            ('primaria', 'Primaria'),
            ('secundaria', 'Secundaria'),
        ],
        blank=True,
        null=True,
        verbose_name='Nivel (Colegios)'
    )
    grado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Grado (Colegios)')
    seccion = models.CharField(max_length=50, blank=True, null=True, verbose_name='Sección (Colegios)')
    
    # Campos específicos para empresas
    razon_social = models.CharField(max_length=200, blank=True, null=True, verbose_name='Razón Social')
    
    # Estado del cliente
    activo = models.BooleanField(default=True, verbose_name='Activo')
    
    # Fechas importantes
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellidos', 'nombres']
        unique_together = ['tenant', 'dni']
    
    def __str__(self):
        if self.tipo_cliente == 'empresa' and self.razon_social:
            return f"{self.razon_social} - {self.obtener_nombre_completo()}"
        return self.obtener_nombre_completo()
    
    def obtener_nombre_completo(self):
        """Obtener nombre completo del cliente"""
        return f"{self.nombres} {self.apellidos}".strip()
    
    def clean(self):
        """Validaciones personalizadas"""
        # Validar campos requeridos según tipo de cliente
        if self.tipo_cliente == 'empresa' and not self.razon_social:
            raise ValidationError({'razon_social': 'La razón social es obligatoria para empresas'})
        
        # Validar formato de DNI/RUC
        if self.dni:
            self.dni = self.dni.strip()
            if not self.dni.replace('-', '').replace(' ', '').isalnum():
                raise ValidationError({'dni': 'El DNI/RUC debe contener solo números, letras y guiones'})
    
    def save(self, *args, **kwargs):
        """Guardar con validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)


class Contrato(models.Model):
    """
    Modelo para contratos de servicios fotográficos
    Relacionado con pedidos cuando el tipo de documento es 'Contrato'
    """
    ESTADO_CONTRATO_CHOICES = [
        ('borrador', 'Borrador'),
        ('activo', 'Activo'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Estudio Fotográfico')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente', related_name='contratos')
    
    # Información del contrato
    numero_contrato = models.CharField(max_length=50, verbose_name='Número de Contrato')
    titulo = models.CharField(max_length=200, verbose_name='Título del Contrato')
    descripcion = models.TextField(verbose_name='Descripción')
    
    # Fechas importantes
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_fin = models.DateField(verbose_name='Fecha de Fin')
    
    # Montos
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Total')
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CONTRATO_CHOICES,
        default='borrador',
        verbose_name='Estado'
    )
    
    # Fechas de registro
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-creado_en']
        unique_together = ['tenant', 'numero_contrato']
    
    def __str__(self):
        return f"{self.numero_contrato} - {self.titulo}"
    
    def clean(self):
        """Validaciones personalizadas"""
        if self.fecha_inicio and self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            raise ValidationError({'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio'})
    
    def save(self, *args, **kwargs):
        """Guardar con validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)