from django.contrib import admin
from .models import OrdenProduccion
from base.models import CustomUser, Cliente, Inquilino
from pedidos.models import Pedido

@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ('numero_op', 'pedido', 'cliente', 'tipo', 'estado', 'prioridad', 
                   'operario', 'fecha_estimada', 'id_inquilino')
    list_filter = ('estado', 'tipo', 'prioridad', 'id_inquilino')
    search_fields = ('numero_op', 'pedido__codigo', 'descripcion', 'cliente__nombre')
    date_hierarchy = 'fecha_estimada'
    readonly_fields = ('creado_en', 'actualizado_en')
    
    def get_fields(self, request, obj=None):
        """Ocultar id_inquilino para usuarios no superusuarios"""
        fields = list(super().get_fields(request, obj))
        
        # Si no es superusuario, ocultar id_inquilino
        if not request.user.is_superuser and 'id_inquilino' in fields:
            fields.remove('id_inquilino')
        
        return fields
    
    def get_readonly_fields(self, request, obj=None):
        """Hacer readonly algunos campos según el usuario"""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        # Para superusuarios, mostrar id_inquilino pero como readonly si ya existe el objeto
        if request.user.is_superuser and obj:
            if 'id_inquilino' not in readonly_fields:
                readonly_fields.append('id_inquilino')
        
        return readonly_fields
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtrar campos relacionados según el inquilino del usuario.
        Corrige el KeyError: 'queryset' asegurando que siempre exista un queryset base.
        """
        
        # Obtener el queryset base del campo
        if 'queryset' not in kwargs:
            kwargs['queryset'] = db_field.remote_field.model.objects.all()
        
        # Filtrar pedidos por inquilino
        if db_field.name == "pedido":
            if request.user.is_superuser:
                # Superusuarios ven todos los pedidos
                kwargs["queryset"] = Pedido.objects.all()
            elif hasattr(request.user, 'id_inquilino') and request.user.id_inquilino:
                # Usuarios normales solo ven pedidos de su inquilino
                kwargs["queryset"] = Pedido.objects.filter(id_inquilino=request.user.id_inquilino)
            else:
                # Usuario sin inquilino asignado - mostrar lista vacía
                kwargs["queryset"] = Pedido.objects.none()
        
        # Filtrar clientes por inquilino
        elif db_field.name == "cliente":
            if request.user.is_superuser:
                # Superusuarios ven todos los clientes
                kwargs["queryset"] = Cliente.objects.all()
            elif hasattr(request.user, 'id_inquilino') and request.user.id_inquilino:
                # Usuarios normales solo ven clientes de su inquilino
                kwargs["queryset"] = Cliente.objects.filter(id_inquilino=request.user.id_inquilino)
            else:
                # Usuario sin inquilino asignado - mostrar lista vacía
                kwargs["queryset"] = Cliente.objects.none()
        
        # Filtrar operarios por rol e inquilino
        elif db_field.name == "operario":
            if request.user.is_superuser:
                # Superusuarios ven todos los operarios
                kwargs["queryset"] = CustomUser.objects.filter(rol='Operario')
            elif hasattr(request.user, 'id_inquilino') and request.user.id_inquilino:
                # Usuarios normales solo ven operarios de su inquilino
                kwargs["queryset"] = CustomUser.objects.filter(
                    rol='Operario',
                    id_inquilino=request.user.id_inquilino
                )
            else:
                # Usuario sin inquilino asignado - mostrar lista vacía
                kwargs["queryset"] = CustomUser.objects.none()
        
        # Filtrar inquilinos
        elif db_field.name == "id_inquilino":
            if request.user.is_superuser:
                # Superusuarios ven todos los inquilinos
                kwargs["queryset"] = Inquilino.objects.all()
            elif hasattr(request.user, 'id_inquilino') and request.user.id_inquilino:
                # Usuarios normales solo ven su inquilino
                kwargs["queryset"] = Inquilino.objects.filter(id=request.user.id_inquilino.id)
            else:
                # Usuario sin inquilino asignado - mostrar lista vacía
                kwargs["queryset"] = Inquilino.objects.none()
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        """Filtrar órdenes por inquilino del usuario"""
        qs = super().get_queryset(request)
        
        # Superusuarios ven todas las órdenes
        if request.user.is_superuser:
            return qs
        
        # Usuarios normales solo ven de su inquilino
        if hasattr(request.user, 'id_inquilino') and request.user.id_inquilino:
            return qs.filter(id_inquilino=request.user.id_inquilino)
        
        # Usuario sin inquilino asignado - no ve nada
        return qs.none()
    
    def save_model(self, request, obj, form, change):
        """Asignar automáticamente el inquilino del usuario"""
        
        # Si no es superusuario, asignar automáticamente su inquilino
        if not request.user.is_superuser:
            if hasattr(request.user, 'id_inquilino') and request.user.id_inquilino:
                obj.id_inquilino = request.user.id_inquilino
        
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        """Verificar permisos para agregar órdenes"""
        # Usuarios sin inquilino no pueden crear órdenes
        if not request.user.is_superuser:
            if not (hasattr(request.user, 'id_inquilino') and request.user.id_inquilino):
                return False
        return super().has_add_permission(request)
    
    def has_change_permission(self, request, obj=None):
        """Verificar permisos para modificar órdenes"""
        if not request.user.is_superuser and obj:
            # Solo puede modificar órdenes de su inquilino
            if hasattr(request.user, 'id_inquilino') and request.user.id_inquilino:
                return obj.id_inquilino == request.user.id_inquilino
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        """Verificar permisos para eliminar órdenes"""
        if not request.user.is_superuser and obj:
            # Solo puede eliminar órdenes de su inquilino
            if hasattr(request.user, 'id_inquilino') and request.user.id_inquilino:
                return obj.id_inquilino == request.user.id_inquilino
            return False
        return super().has_delete_permission(request, obj)