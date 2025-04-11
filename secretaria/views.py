from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from secretaria.models import Aluno
from secretaria.utils import GeneratorPdf


class ContratoAlunosPdfView(View, GeneratorPdf):
    def get(self, request, *args, **kwargs):
        alunos = Aluno.objects.all()
        dados = {
            'alunos': alunos,
        }

        pdf = self.render_to_pdf('contrato_pdf.html', dados)
        return HttpResponse(pdf, content_type='application/pdf')
