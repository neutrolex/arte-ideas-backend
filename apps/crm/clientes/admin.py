from django.contrib import admin, messages
from .models import Cliente
from .forms import ClienteForm


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForm

    list_display = (
        'nombre_completo', 'tipo_cliente', 'telefono_contacto',
        'direccion', 'pedidos', 'total_gastado', 'ultima_fecha_pedido'
    )
    list_filter = ('tipo_cliente',)
    search_fields = ('nombre_completo', 'dni', 'email')
    ordering = ('nombre_completo',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            self.message_user(
                request,
                "Cliente registrado con éxito.",
                level=messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                f"Cliente '{obj.nombre_completo}' actualizado con éxito.",
                level=messages.SUCCESS
            )

    class Media:
        js = ('admin/js/cliente_fields_toggle.js',)