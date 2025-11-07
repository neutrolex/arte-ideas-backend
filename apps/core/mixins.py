# apps/core/mixins.py
from rest_framework.decorators import action
from rest_framework.response import Response

class ExportMixin:


    @action(detail=False, methods=['post'], url_path='export')
    def export(self, request, *args, **kwargs):
      
        
        export_format = request.data.get('format', 'pdf').lower()
        filters = request.data.get('filters', {})
      
        if export_format not in ['pdf', 'excel', 'csv']:
            return Response(
                {"error": "Formato no soportado. Use 'pdf', 'excel' o 'csv'."}, 
                status=400
            )

        print(f"Iniciando exportación en formato {export_format}...")
        print(f"Filtros aplicados: {filters}")
        
        return Response({
            "message": f"Exportación en formato '{export_format}' iniciada.",
            "status": "pending",
            "filters_received": filters,
            "info": "Esta es una respuesta temporal. Implementar la lógica completa."
        })
        