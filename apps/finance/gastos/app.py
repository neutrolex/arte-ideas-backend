# apps/finance/gastos/app.py

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GastosConfig(AppConfig):
   
    name = 'apps.finance.gastos'
    verbose_name = _('Sub-Módulo de Gastos')
