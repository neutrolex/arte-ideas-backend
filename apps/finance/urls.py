from django.urls import path, include
# Las vistas se importan automáticamente a través del índice views.py

app_name = 'finance'

urlpatterns = [
    # Incluye el archivo de URLs de la subcarpeta 'gastos/'
    # Se recomienda que el archivo dentro de gastos se llame urls.py 
    path('', include('apps.finance.gastos.urls')), 
]