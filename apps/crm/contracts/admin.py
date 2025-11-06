from django.contrib import admin, messages

from .models import Contrato
from apps.crm.models import Cliente
from .services import ContractPDFService, PDFNotImplemented


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo', 'tipo_contrato', 'estado', 'monto',
        'fecha_inicio', 'fecha_fin', 'cliente', 'nombre_cliente'
    )
    list_filter = ('tipo_contrato', 'estado', 'fecha_inicio')
    search_fields = ('titulo', 'nombre_cliente', 'referencia_externa')
    ordering = ('-fecha_inicio',)
    exclude = ('tenant',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if getattr(user, 'is_superuser', False):
            return qs
        return qs.filter(tenant=user.tenant)

    def save_model(self, request, obj, form, change):
        if not change or obj.tenant_id is None:
            obj.tenant = request.user.tenant
        super().save_model(request, obj, form, change)

        self.message_user(
            request,
            ("Contrato creado con éxito." if not change else f"Contrato '{obj.titulo}' actualizado con éxito."),
            level=messages.SUCCESS
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'cliente' and request and hasattr(request, 'user') and not request.user.is_superuser:
            kwargs['queryset'] = Cliente.objects.filter(tenant=request.user.tenant)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    actions = ['generar_pdf']

    def generar_pdf(self, request, queryset):
        success = 0
        not_impl = 0
        for contrato in queryset:
            try:
                ContractPDFService.generate(contrato)
                success += 1
            except PDFNotImplemented:
                not_impl += 1
        if success:
            self.message_user(request, f'Se generó PDF para {success} contrato(s).', level=messages.SUCCESS)
        if not_impl:
            self.message_user(request, f'PDF no disponible para {not_impl} contrato(s): weasyprint no instalado.', level=messages.WARNING)
    generar_pdf.short_description = 'Generar PDF de contrato'