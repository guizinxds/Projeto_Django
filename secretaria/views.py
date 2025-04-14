from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


from secretaria.models import Aluno
from secretaria.utils import GeneratorPdf


class ContratoAlunosPdfView(View, GeneratorPdf):
    def get(self, request, aluno_id, *args, **kwargs):
        aluno = get_object_or_404(Aluno, id=aluno_id)
        dados = {
            'aluno': aluno,
        }

        pdf = self.render_to_pdf('contrato_pdf.html', dados)
        return HttpResponse(pdf, content_type='application/pdf')
    


