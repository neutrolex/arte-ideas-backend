"""
Modelos del CRM App - Arte Ideas
Gestión de clientes y relaciones comerciales
"""
from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import Tenant


class Client(models.Model):
    """
    Modelo para clientes del estudio fotográfico
    Soporta diferentes tipos de clientes: Particular, Colegio, Empresa
    """
    CLIENT_TYPE_CHOICES = [
        ('particular', 'Particular'),
        ('colegio', 'Colegio'),
        ('empresa', 'Empresa'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Estudio Fotográfico')
    
    # Información básica del cliente
    client_type = models.CharField(
        max_length=20, 
        choices=CLIENT_TYPE_CHOICES, 
        default='particular',
        verbose_name='Tipo de Cliente'
    )
    first_name = models.CharField(max_length=100, verbose_name='Nombres')
    last_name = models.CharField(max_length=100, verbose_name='Apellidos')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=15, verbose_name='Teléfono')
    dni = models.CharField(max_length=15, verbose_name='DNI/RUC', unique=True)
    address = models.TextField(verbose_name='Dirección')
    
    # Campos específicos para colegios
    school_level = models.CharField(
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
    grade = models.CharField(max_length=50, blank=True, null=True, verbose_name='Grado (Colegios)')
    section = models.CharField(max_length=50, blank=True, null=True, verbose_name='Sección (Colegios)')
    
    # Campos específicos para empresas
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Razón Social')
    
    # Estado del cliente
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    # Fechas importantes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['last_name', 'first_name']
        unique_together = ['tenant', 'dni']
    
    def __str__(self):
        if self.client_type == 'empresa' and self.company_name:
            return f"{self.company_name} - {self.get_full_name()}"
        return self.get_full_name()
    
    def get_full_name(self):
        """Obtener nombre completo del cliente"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def clean(self):
        """Validaciones personalizadas"""
        # Validar campos requeridos según tipo de cliente
        if self.client_type == 'empresa' and not self.company_name:
            raise ValidationError({'company_name': 'La razón social es obligatoria para empresas'})
        
        # Validar formato de DNI/RUC
        if self.dni:
            self.dni = self.dni.strip()
            if not self.dni.replace('-', '').replace(' ', '').isalnum():
                raise ValidationError({'dni': 'El DNI/RUC debe contener solo números, letras y guiones'})
    
    def save(self, *args, **kwargs):
        """Guardar con validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)


class Contract(models.Model):
    """
    Modelo para contratos de servicios fotográficos
    Relacionado con pedidos cuando el tipo de documento es 'Contrato'
    """
    CONTRACT_STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('active', 'Activo'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Estudio Fotográfico')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente', related_name='contracts')
    
    # Información del contrato
    contract_number = models.CharField(max_length=50, verbose_name='Número de Contrato')
    title = models.CharField(max_length=200, verbose_name='Título del Contrato')
    description = models.TextField(verbose_name='Descripción')
    
    # Fechas importantes
    start_date = models.DateField(verbose_name='Fecha de Inicio')
    end_date = models.DateField(verbose_name='Fecha de Fin')
    
    # Montos
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Total')
    
    # Estado
    status = models.CharField(
        max_length=20,
        choices=CONTRACT_STATUS_CHOICES,
        default='draft',
        verbose_name='Estado'
    )
    
    # Fechas de registro
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-created_at']
        unique_together = ['tenant', 'contract_number']
    
    def __str__(self):
        return f"{self.contract_number} - {self.title}"
    
    def clean(self):
        """Validaciones personalizadas"""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({'end_date': 'La fecha de fin debe ser posterior a la fecha de inicio'})
    
    def save(self, *args, **kwargs):
        """Guardar con validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)