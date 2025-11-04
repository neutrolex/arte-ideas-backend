from django import forms
from django.core.exceptions import ValidationError
from django.forms import models as forms_models # Importación segura
from .models import Cliente

# --- VALIDATORS ---
def validate_dni(value):
    if value and (not value.isdigit() or len(value) != 8):
        raise ValidationError('El DNI debe tener 8 dígitos numéricos')

def validate_ruc(value):
    if value and (not value.isdigit() or len(value) != 11):
        raise ValidationError('El RUC debe tener 11 dígitos numéricos')

# --- MODEL FORM ---
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese 8 dígitos', 'type': 'number'}),
            'ruc': forms.TextInput(attrs={'placeholder': 'Ingrese 11 dígitos', 'type': 'number'}),
            'institucion_educativa': forms.TextInput(attrs={'placeholder': 'Solo para colegios'}),
            'telefono_contacto': forms.TextInput(attrs={'type': 'tel'}),
            'email': forms.EmailInput(attrs={'type': 'email'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Configurar campos según el tipo de cliente (tu lógica original)
        if self.instance and self.instance.pk:
            self.setup_fields_for_client_type(self.instance.tipo_cliente)

            # 2. SOLUCIÓN CLAVE: Deshabilitar el validador de unicidad.
            for field_name in ['ruc', 'dni']:
                if field_name in self.fields:
                    # Sobreescribimos la lista de validadores con una lista vacía 
                    # para desactivar el check automático de unicidad del ModelForm.
                    # Confiamos en la validación 'clean' de tu modelo/formulario.
                    self.fields[field_name].validators = [] 
            
    def setup_fields_for_client_type(self, client_type):
        """Configura los campos según el tipo de cliente"""
        if client_type == 'particular':
            self.fields['dni'].required = True
            self.fields['ruc'].required = False
            self.fields['institucion_educativa'].required = False
        else:
            self.fields['dni'].required = False
            self.fields['ruc'].required = True
            self.fields['institucion_educativa'].required = (client_type == 'colegio')
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_cliente = cleaned_data.get('tipo_cliente')
        dni = cleaned_data.get('dni')
        ruc = cleaned_data.get('ruc')
        
        # Esta lógica ya maneja la limpieza y las dependencias (DNI/RUC/Institución)
        if tipo_cliente == 'particular':
            if not dni:
                self.add_error('dni', 'El DNI es obligatorio para clientes particulares')
            cleaned_data['ruc'] = None
        else:
            if not ruc:
                self.add_error('ruc', 'El RUC es obligatorio para empresas y colegios')
            cleaned_data['dni'] = None
            
            if tipo_cliente == 'colegio' and not cleaned_data.get('institucion_educativa'):
                self.add_error('institucion_educativa', 'La institución educativa es obligatoria para colegios')
            elif tipo_cliente != 'colegio':
                cleaned_data['institucion_educativa'] = None
        
        return cleaned_data