# Generated migration to unify models in Spanish
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_rolepermission_role_alter_user_role'),
        ('crm', '0001_initial'),
    ]

    operations = [
        # Renombrar modelo Client a Cliente
        migrations.RenameModel(
            old_name='Client',
            new_name='Cliente',
        ),
        
        # Renombrar modelo Contract a Contrato
        migrations.RenameModel(
            old_name='Contract',
            new_name='Contrato',
        ),
        
        # Renombrar campos del modelo Cliente
        migrations.RenameField(
            model_name='cliente',
            old_name='client_type',
            new_name='tipo_cliente',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='first_name',
            new_name='nombres',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='last_name',
            new_name='apellidos',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='phone',
            new_name='telefono',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='address',
            new_name='direccion',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='school_level',
            new_name='nivel_educativo',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='grade',
            new_name='grado',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='section',
            new_name='seccion',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='company_name',
            new_name='razon_social',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='is_active',
            new_name='activo',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='created_at',
            new_name='creado_en',
        ),
        migrations.RenameField(
            model_name='cliente',
            old_name='updated_at',
            new_name='actualizado_en',
        ),
        
        # Renombrar campos del modelo Contrato
        migrations.RenameField(
            model_name='contrato',
            old_name='client',
            new_name='cliente',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='contract_number',
            new_name='numero_contrato',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='title',
            new_name='titulo',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='description',
            new_name='descripcion',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='start_date',
            new_name='fecha_inicio',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='end_date',
            new_name='fecha_fin',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='total_amount',
            new_name='monto_total',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='status',
            new_name='estado',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='created_at',
            new_name='creado_en',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='updated_at',
            new_name='actualizado_en',
        ),
        
        # Actualizar choices en español
        migrations.AlterField(
            model_name='cliente',
            name='tipo_cliente',
            field=models.CharField(
                choices=[('particular', 'Particular'), ('colegio', 'Colegio'), ('empresa', 'Empresa')],
                default='particular',
                max_length=20,
                verbose_name='Tipo de Cliente'
            ),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='estado',
            field=models.CharField(
                choices=[('borrador', 'Borrador'), ('activo', 'Activo'), ('completado', 'Completado'), ('cancelado', 'Cancelado')],
                default='borrador',
                max_length=20,
                verbose_name='Estado'
            ),
        ),
        
        # Actualizar Meta options
        migrations.AlterModelOptions(
            name='cliente',
            options={
                'ordering': ['apellidos', 'nombres'],
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes'
            },
        ),
        migrations.AlterModelOptions(
            name='contrato',
            options={
                'ordering': ['-creado_en'],
                'verbose_name': 'Contrato',
                'verbose_name_plural': 'Contratos'
            },
        ),
    ]