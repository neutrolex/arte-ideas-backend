from django.apps import AppConfig


class ContractsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.crm.contracts"
    verbose_name = "Contratos (CRM)"

    def ready(self):
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass