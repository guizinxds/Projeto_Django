from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse

from secretaria.models import *
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
    materia_param = request.GET.get('materia')

    turma_selecionada = None
    materia_selecionada = None

    # Turma por ID (int)
    if turma_param:
        try:
            turma_selecionada = Turma.objects.get(id=int(turma_param))
        except (ValueError, Turma.DoesNotExist):
            turma_selecionada = None

    # Matéria por ID (int)
    if materia_param:
        try:
            materia_selecionada = Materia.objects.get(id=int(materia_param))
        except (ValueError, Materia.DoesNotExist):
            materia_selecionada = None

    filtro = {}
    if turma_selecionada:
        filtro['turma'] = turma_selecionada
    if materia_selecionada:
        filtro['materia'] = materia_selecionada

    notas_1bim = Nota1Bim.objects.filter(**filtro)
    notas_2bim = Nota2Bim.objects.filter(**filtro)
    notas_3bim = Nota3Bim.objects.filter(**filtro)
    notas_4bim = Nota4Bim.objects.filter(**filtro)

    turmas = Turma.objects.all()
    materias_ids = Nota1Bim.objects.values_list('materia', flat=True).distinct()
    materias = Materia.objects.filter(id__in=materias_ids)

    return render(request, 'notas/tabela_notas.html', {
        'turmas': turmas,
        'materias': materias,
        'turma_selecionada': turma_selecionada,
        'materia_selecionada': materia_selecionada,
        'notas_1bim': notas_1bim,
        'notas_2bim': notas_2bim,
        'notas_3bim': notas_3bim,
        'notas_4bim': notas_4bim,
    })
