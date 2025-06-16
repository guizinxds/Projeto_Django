from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.template.loader import get_template

from xhtml2pdf import pisa

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



#filtro para notas
def notas_por_bimestre(request):
    turma_param = request.GET.get('turma')
    materia_param = request.GET.get('materia')

    turma_selecionada = None
    materia_selecionada = None

    # turma por ID 
    if turma_param:
        try:
            turma_selecionada = Turma.objects.get(id=int(turma_param))
        except (ValueError, Turma.DoesNotExist):
            turma_selecionada = None

    # materia por ID 
    if materia_param:
        try:
            materia_selecionada = Materia.objects.get(id=int(materia_param))
        except (ValueError, Materia.DoesNotExist):
            materia_selecionada = None


    #aqui é onde o filtro é iniciado
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

#portal do estudante

# página inicial do portal

@login_required
def dashboard(request):

    try:
        perfil = request.user.perfil
    except:
        logout(request)
        messages.error(request, "Seu perfil não está configurado. Contate a administração")
        return redirect('dashboard')
    
    context = {
        'perfil' : perfil,
    }

    return render(request, 'portal/dashboard.html', context)


# página onde o usuário consegue ver suas respectivas notas

@login_required
def minhas_notas(request):
    perfil = request.user.perfil

    if not perfil.aluno:
        return HttpResponse("Apenas alunos tem acesso as notas")
    
    notas_1bim = Nota1Bim.objects.filter(aluno=perfil.aluno)
    notas_2bim = Nota2Bim.objects.filter(aluno=perfil.aluno)
    notas_3bim = Nota3Bim.objects.filter(aluno=perfil.aluno)
    notas_4bim = Nota4Bim.objects.filter(aluno=perfil.aluno)


    bimestres =[
        ('1º Bimestre', notas_1bim),
        ('2º Bimestre', notas_2bim),
        ('3º Bimestre', notas_3bim),
        ('4º Bimestre', notas_4bim),
    ]

    context ={
        'perfil': perfil,
        'bimestres':bimestres,
    }

    return render(request, 'portal/minhas_notas.html', context)


# página onde o usuário vê as informações de pagamento da mensalidade

@login_required
def mensalidade(request):
    perfil = request.user.perfil

    if perfil.aluno:
        mensalidades = Mensalidade.objects.filter(aluno=perfil.aluno)
    elif perfil.responsavel:
        mensalidades = Mensalidade.objects.filter(responsavel=perfil.responsavel)
    else:
        mensalidades = Mensalidade.objects.none()

    #será conferido se a mensalidade está paga ou não
    mensalidades_pagas = mensalidades.filter(pago=True).order_by('data_pagamento')
    mensalidades_pendentes = mensalidades.filter(pago=False).order_by('data_pagamento')

    context = {
        'perfil': perfil,
        'mensalidades_pagas': mensalidades_pagas,
        'mensalidades_pendentes': mensalidades_pendentes,
    }

    return render(request, 'portal/minhas_mensalidades.html', context)


# página onde o usuário consegue ver os eventos que acontecerão 

@login_required
def eventos(request):
    eventos = Evento.objects.all()

    context = {
        'eventos': eventos,
    }

    return render(request, 'portal/eventos.html', context)

def home(request):
    return render(request, 'home.html')



# função que gera o pdf do boleto

def gerar_boleto(request, mensalidade_id):
    mensalidade = get_object_or_404(Mensalidade, id=mensalidade_id)

    template = get_template('boleto.html')
    html = template.render({'mensalidade':mensalidade})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=mensalidade_{mensalidade_id}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response





    