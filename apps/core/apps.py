from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Core - Sistema Base'
    
    def ready(self):
        """
        Código que se ejecuta cuando la app está lista
        """
        # Importar signals si los hay
        try:
            import apps.core.signals
        except ImportError:
            pass