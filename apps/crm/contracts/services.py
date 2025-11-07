from django.template.loader import render_to_string
from django.core.files.base import ContentFile


class PDFNotImplemented(Exception):
    pass


class ContractPDFService:
    template_name = 'exports/contract.html'

    @classmethod
    def generate(cls, contract):
        try:
            from weasyprint import HTML  # optional dependency
        except Exception:
            raise PDFNotImplemented()

        html_content = render_to_string(cls.template_name, {'contract': contract})
        pdf_bytes = HTML(string=html_content).write_pdf()
        filename = f"contract_{contract.id}.pdf"
        contract.document.save(filename, ContentFile(pdf_bytes), save=True)
        return contract.document