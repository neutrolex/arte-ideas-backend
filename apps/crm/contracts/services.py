from django.template.loader import render_to_string


class ContractPDFService:
    def __init__(self, tenant, user=None):
        self.tenant = tenant
        self.user = user

    def generate_contract(self, contract):
        # Importar WeasyPrint de forma perezosa para evitar errores de entorno
        try:
            from weasyprint import HTML  # noqa: WPS433
        except Exception as e:
            raise RuntimeError(f"WeasyPrint no disponible: {e}")

        html = render_to_string(
            "exports/contract.html", {"contract": contract, "tenant": self.tenant}
        )
        pdf_bytes = HTML(string=html).write_pdf()
        filename = f"{contract.id}-{contract.title}.pdf"
        # Guardar el PDF en el FileField del contrato
        from django.core.files.base import ContentFile

        contract.document.save(filename, content=ContentFile(pdf_bytes))
        return filename