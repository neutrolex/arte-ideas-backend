from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Contract


@receiver(post_save, sender=Contract)
def contract_post_save(sender, instance, created, **kwargs):
    # Placeholder para integraciones futuras (analytics, operaciones, finanzas)
    return


@receiver(pre_delete, sender=Contract)
def contract_pre_delete(sender, instance, **kwargs):
    # Placeholder para cleanup relacionado al contrato
    return