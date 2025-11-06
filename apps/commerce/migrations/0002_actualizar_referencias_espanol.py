# Generated migration to update Spanish references
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_unificar_modelos_espanol'),
        ('commerce', '0001_initial'),
    ]

    operations = [
        # Renombrar campo client a cliente
        migrations.RenameField(
            model_name='order',
            old_name='client',
            new_name='cliente',
        ),
        
        # Renombrar campo contract a contrato
        migrations.RenameField(
            model_name='order',
            old_name='contract',
            new_name='contrato',
        ),
        
        # Actualizar la referencia del ForeignKey
        migrations.AlterField(
            model_name='order',
            name='cliente',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='pedidos',
                to='crm.cliente',
                verbose_name='Cliente'
            ),
        ),
        
        migrations.AlterField(
            model_name='order',
            name='contrato',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='pedidos',
                to='crm.contrato',
                verbose_name='Contrato Relacionado'
            ),
        ),
    ]