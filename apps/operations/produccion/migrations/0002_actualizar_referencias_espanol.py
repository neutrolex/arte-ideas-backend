# Generated migration to update Spanish references in production
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_unificar_modelos_espanol'),
        ('produccion', '0001_initial'),
    ]

    operations = [
        # Actualizar la referencia del ForeignKey cliente
        migrations.AlterField(
            model_name='ordenproduccion',
            name='cliente',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='ordenes_produccion',
                to='crm.cliente'
            ),
        ),
    ]