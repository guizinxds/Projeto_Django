from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class GeneratorPdf:
    def render_to_pdf(self, template_src, context={}):
        template = get_template(template_src)
        html = template.render(context)
        result = BytesIO()

        try:
            pisa_status = pisa.CreatePDF(
                html, dest=result
            )
            if not pisa_status.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print("Erro ao gerar PDF:", e)

        return None
