from django.contrib import admin, messages # <--- ¡Añadir 'messages' aquí!
from .models import Cliente
from .forms import ClienteForm

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # 2. Asignar el formulario personalizado
    form = ClienteForm 
    
    list_display = ('nombre_completo', 'tipo_cliente', 'telefono_contacto','direccion','pedidos','total_gastado','ultima_fecha_pedido')
    list_filter = ('tipo_cliente',)
    search_fields = ('nombre_completo', 'dni', 'email')
    ordering = ('nombre_completo',)

    # 1. El método save_model debe estar indentado DENTRO de la clase
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # El método 'change' es True si es una edición, False si es un nuevo registro
        if not change:
            # Mostrar el mensaje personalizado solo para nuevos registros
            self.message_user(
                request, 
                "Cliente registrado con éxito.", 
                level=messages.SUCCESS # Tipo de mensaje (verde)
            )
        else:
            # Mensaje para ediciones
            self.message_user(
                request,
                f"Cliente '{obj.nombre_completo}' actualizado con éxito.",
                level=messages.SUCCESS
            )
    
    # La clase Media debe estar indentada DENTRO de la clase
    class Media:
        # La ruta es relativa a la carpeta 'static' dentro de la app (clientes/static/...)
        js = ('admin/js/cliente_fields_toggle.js',)