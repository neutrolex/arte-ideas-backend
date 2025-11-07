"""
URLs del CRM App - Arte Ideas
"""
from django.urls import path, include

app_name = 'crm'

urlpatterns = [
    # Submódulo Clientes
    path('clients/', include('apps.crm.clientes.urls')),
    # Submódulo Contratos
    path('contracts/', include('apps.crm.contracts.urls')),
    # Submódulo Agenda
    path('agenda/', include('apps.crm.agenda.urls')),
]