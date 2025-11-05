from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Evento, Cita, Recordatorio


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo_evento', 'fecha_inicio', 'fecha_fin', 'prioridad', 'estado', 'asignado_a', 'cliente_link']
    list_filter = ['tipo_evento', 'prioridad', 'estado', 'es_todo_el_dia', 'fecha_inicio', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'ubicacion', 'cliente__nombre_completo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'duracion_minutos', 'esta_vencido']

    def cliente_link(self, obj):
        if obj.cliente:
            url = reverse('admin:clientes_cliente_change', args=[obj.cliente.id])
            return format_html('<a href="{}">{}</a>', url, obj.cliente.nombre_completo)
        return "-"
    cliente_link.short_description = 'Cliente'


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['evento', 'cliente', 'motivo', 'estado_cita', 'valor_oportunidad', 'probabilidad_cierre']
    list_filter = ['motivo', 'estado_cita', 'evento__fecha_inicio', 'recordatorio_enviado', 'confirmacion_enviada']
    search_fields = ['evento__titulo', 'cliente__nombre_completo', 'contacto_cliente', 'resultado']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ['evento', 'tipo_recordatorio', 'minutos_antes', 'enviado', 'destinatario']
    list_filter = ['tipo_recordatorio', 'enviado', 'fecha_creacion', 'fecha_envio']
    search_fields = ['evento__titulo', 'mensaje', 'destinatario__username']