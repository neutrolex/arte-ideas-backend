"""
Admin configuration for CRM App - Arte Ideas
Configuración del panel de administración para modelos de CRM
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone

from .models import Client, Contract


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Administración de Clientes"""
    
    list_display = [
        'full_name', 'client_type', 'email', 'phone', 'dni',
        'company_info', 'school_info', 'created_at_formatted'
    ]
    list_filter = [
        'client_type', 'created_at', 'updated_at'
    ]
    search_fields = [
        'first_name', 'last_name', 'email', 'phone', 'dni',
        'company_name', 'ruc', 'school_level', 'school_grade'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información Personal', {
            'fields': (
                'client_type', 'first_name', 'last_name',
                'email', 'phone', 'dni', 'address'
            )
        }),
        ('Información de Empresa', {
            'fields': ('company_name', 'ruc'),
            'classes': ('collapse',)
        }),
        ('Información de Colegio', {
            'fields': ('school_level', 'school_grade', 'school_section'),
            'classes': ('collapse',)
        }),
        ('Información Adicional', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_at_formatted', 'updated_at_formatted'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at_formatted', 'updated_at_formatted']
    
    def full_name(self, obj):
        """Nombre completo del cliente"""
        return f"{obj.first_name} {obj.last_name}"
    
    full_name.short_description = 'Nombre Completo'
    full_name.admin_order_field = 'first_name'
    
    def company_info(self, obj):
        """Información de empresa"""
        if obj.client_type == 'empresa' and obj.company_name:
            return mark_safe(f'<span style="color: blue;">{obj.company_name}<br/>RUC: {obj.ruc}</span>')
        return '-'
    
    company_info.short_description = 'Empresa'
    
    def school_info(self, obj):
        """Información de colegio"""
        if obj.client_type == 'colegio':
            return mark_safe(f'<span style="color: green;">{obj.school_level}<br/>{obj.school_grade} - {obj.school_section}</span>')
        return '-'
    
    school_info.short_description = 'Colegio'
    
    def created_at_formatted(self, obj):
        """Fecha de creación formateada"""
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    
    created_at_formatted.short_description = 'Creado el'
    
    def updated_at_formatted(self, obj):
        """Fecha de actualización formateada"""
        return obj.updated_at.strftime('%d/%m/%Y %H:%M') if obj.updated_at else '-'
    
    updated_at_formatted.short_description = 'Actualizado el'
    
    def get_queryset(self, request):
        """Sobrescribir queryset para optimizar"""
        qs = super().get_queryset(request)
        return qs.annotate(
            contract_count=Count('contracts')
        )
    
    def client_type_indicator(self, obj):
        """Indicador visual de tipo de cliente"""
        indicators = {
            'particular': mark_safe('<span style="color: blue;">👤 Particular</span>'),
            'empresa': mark_safe('<span style="color: green;">🏢 Empresa</span>'),
            'colegio': mark_safe('<span style="color: purple;">🏫 Colegio</span>')
        }
        return indicators.get(obj.client_type, obj.client_type)
    
    client_type_indicator.short_description = 'Tipo'
    
    actions = ['mark_as_particular', 'mark_as_empresa', 'mark_as_colegio', 'export_clients']
    
    def mark_as_particular(self, request, queryset):
        """Marcar clientes como particulares"""
        updated = queryset.update(client_type='particular')
        self.message_user(request, f'{updated} cliente(s) marcado(s) como particular(es).', messages.SUCCESS)
    
    mark_as_particular.short_description = "Marcar como particulares"
    
    def mark_as_empresa(self, request, queryset):
        """Marcar clientes como empresas"""
        updated = queryset.update(client_type='empresa')
        self.message_user(request, f'{updated} cliente(s) marcado(s) como empresa(s).', messages.SUCCESS)
    
    mark_as_empresa.short_description = "Marcar como empresas"
    
    def mark_as_colegio(self, request, queryset):
        """Marcar clientes como colegios"""
        updated = queryset.update(client_type='colegio')
        self.message_user(request, f'{updated} cliente(s) marcado(s) como colegio(s).', messages.SUCCESS)
    
    mark_as_colegio.short_description = "Marcar como colegios"
    
    def export_clients(self, request, queryset):
        """Exportar información de clientes"""
        client_count = queryset.count()
        self.message_user(
            request,
            f'Exportando {client_count} cliente(s). Esta función requiere implementación adicional.',
            messages.INFO
        )
    
    export_clients.short_description = "Exportar clientes"


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """Administración de Contratos"""
    
    list_display = [
        'contract_number', 'client_link', 'title', 'total_amount',
        'status_indicator', 'date_range', 'days_remaining', 'created_at_formatted'
    ]
    list_filter = [
        'status', 'created_at', 'start_date', 'end_date'
    ]
    search_fields = [
        'contract_number', 'title', 'description',
        'client__first_name', 'client__last_name', 'client__company_name'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información del Contrato', {
            'fields': (
                'contract_number', 'client', 'title', 'description'
            )
        }),
        ('Período del Contrato', {
            'fields': (
                'start_date', 'end_date', 'date_range'
            )
        }),
        ('Información Financiera', {
            'fields': (
                'total_amount', 'status'
            )
        }),
        ('Auditoría', {
            'fields': (
                'created_at_formatted', 'updated_at_formatted'
            ),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = [
        'date_range', 'days_remaining', 'created_at_formatted', 'updated_at_formatted'
    ]
    
    def client_link(self, obj):
        """Enlace al cliente"""
        if obj.client:
            url = reverse('admin:crm_client_change', args=[obj.client.id])
            return format_html('<a href="{}">{}</a>', url, str(obj.client))
        return '-'
    
    client_link.short_description = 'Cliente'
    client_link.admin_order_field = 'client'
    
    def status_indicator(self, obj):
        """Indicador visual de estado"""
        status_colors = {
            'pending': 'orange',
            'active': 'green',
            'expired': 'red',
            'cancelled': 'gray'
        }
        
        status_labels = {
            'pending': 'Pendiente',
            'active': 'Activo',
            'expired': 'Vencido',
            'cancelled': 'Cancelado'
        }
        
        color = status_colors.get(obj.status, 'gray')
        label = status_labels.get(obj.status, obj.status)
        
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">● {label}</span>')
    
    status_indicator.short_description = 'Estado'
    
    def date_range(self, obj):
        """Rango de fechas del contrato"""
        if obj.start_date and obj.end_date:
            return f"{obj.start_date.strftime('%d/%m/%Y')} - {obj.end_date.strftime('%d/%m/%Y')}"
        return '-'
    
    date_range.short_description = 'Período'
    
    def days_remaining(self, obj):
        """Días restantes para vencimiento"""
        if obj.end_date and obj.status == 'active':
            today = timezone.now().date()
            days_left = (obj.end_date - today).days
            
            if days_left < 0:
                return mark_safe('<span style="color: red; font-weight: bold;">⚠️ Vencido</span>')
            elif days_left <= 30:
                return mark_safe(f'<span style="color: orange; font-weight: bold;">⚡ {days_left} días</span>')
            else:
                return mark_safe(f'<span style="color: green;">✅ {days_left} días</span>')
        
        return '-'
    
    days_remaining.short_description = 'Días Restantes'
    
    def created_at_formatted(self, obj):
        """Fecha de creación formateada"""
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    
    created_at_formatted.short_description = 'Creado el'
    
    def updated_at_formatted(self, obj):
        """Fecha de actualización formateada"""
        return obj.updated_at.strftime('%d/%m/%Y %H:%M') if obj.updated_at else '-'
    
    updated_at_formatted.short_description = 'Actualizado el'
    
    def get_queryset(self, request):
        """Sobrescribir queryset para optimizar"""
        qs = super().get_queryset(request)
        return qs.select_related('client')
    
    actions = [
        'mark_as_active', 'mark_as_expired', 'mark_as_cancelled',
        'check_expiring_contracts', 'export_contracts'
    ]
    
    def mark_as_active(self, request, queryset):
        """Marcar contratos como activos"""
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} contrato(s) marcado(s) como activo(s).', messages.SUCCESS)
    
    mark_as_active.short_description = "Marcar como activos"
    
    def mark_as_expired(self, request, queryset):
        """Marcar contratos como vencidos"""
        updated = queryset.update(status='expired')
        self.message_user(request, f'{updated} contrato(s) marcado(s) como vencido(s).', messages.WARNING)
    
    mark_as_expired.short_description = "Marcar como vencidos"
    
    def mark_as_cancelled(self, request, queryset):
        """Marcar contratos como cancelados"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} contrato(s) marcado(s) como cancelado(s).', messages.ERROR)
    
    mark_as_cancelled.short_description = "Marcar como cancelados"
    
    def check_expiring_contracts(self, request, queryset):
        """Verificar contratos próximos a vencer"""
        from datetime import timedelta
        
        today = timezone.now().date()
        thirty_days_later = today + timedelta(days=30)
        
        expiring_contracts = queryset.filter(
            end_date__gte=today,
            end_date__lte=thirty_days_later,
            status='active'
        ).count()
        
        if expiring_contracts > 0:
            self.message_user(
                request,
                f'⚠️ {expiring_contracts} contrato(s) próximo(s) a vencer (30 días).',
                messages.WARNING
            )
        else:
            self.message_user(
                request,
                '✅ No hay contratos próximos a vencer en los próximos 30 días.',
                messages.SUCCESS
            )
    
    check_expiring_contracts.short_description = "Verificar contratos próximos a vencer"
    
    def export_contracts(self, request, queryset):
        """Exportar información de contratos"""
        contract_count = queryset.count()
        self.message_user(
            request,
            f'Exportando {contract_count} contrato(s). Esta función requiere implementación adicional.',
            messages.INFO
        )
    
    export_contracts.short_description = "Exportar contratos"


# Configuración adicional del admin para CRM
admin.site.site_header = 'Arte Ideas CRM - Administración'
admin.site.site_title = 'Arte Ideas CRM'
admin.site.index_title = 'Panel de Administración CRM'