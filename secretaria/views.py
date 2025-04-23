from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


from secretaria.models import Aluno
from secretaria.models import Responsavel
from secretaria.utils import GeneratorPdf


class ContratoAlunosPdfView(View, GeneratorPdf):
    def get(self, request, aluno_id, responsavel_id, *args, **kwargs):
        aluno = get_object_or_404(Aluno, id=aluno_id)
        responsavel = get_object_or_404(Responsavel, id=responsavel_id)
        dados = {
            'aluno': aluno,
            'responsavel': responsavel,
        }

        pdf = self.render_to_pdf('contrato_pdf.html', dados)
        return HttpResponse(pdf, content_type='application/pdf')
    


