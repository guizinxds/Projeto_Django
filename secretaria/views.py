from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from secretaria.models import *


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
    


def notas_por_bimestre(request):
    turma_param = request.GET.get('turma')
    turma_selecionada = None

    if turma_param:
        # Correção: Usar 'escolha_a_turma'
        turma_selecionada = Turma.objects.filter(escolha_a_turma=turma_param).first()

    if turma_selecionada:
        notas_1bim = Nota1Bim.objects.filter(turma=turma_selecionada)
        notas_2bim = Nota2Bim.objects.filter(turma=turma_selecionada)
        notas_3bim = Nota3Bim.objects.filter(turma=turma_selecionada)
        notas_4bim = Nota4Bim.objects.filter(turma=turma_selecionada)
    else:
        notas_1bim = Nota1Bim.objects.all()
        notas_2bim = Nota2Bim.objects.all()
        notas_3bim = Nota3Bim.objects.all()
        notas_4bim = Nota4Bim.objects.all()

    turmas = Turma.objects.all()

    # CORREÇÃO: Apontar para o template principal CORRETO
    return render(request, 'notas/tabela_notas.html', {
        'turmas': turmas,
        'turma_selecionada': turma_selecionada,
        'notas_1bim': notas_1bim,
        'notas_2bim': notas_2bim,
        'notas_3bim': notas_3bim,
        'notas_4bim': notas_4bim,
    })

    


