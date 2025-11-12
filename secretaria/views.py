from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.shortcuts import resolve_url  # ← IMPORT NECESSÁRIO

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
    # Bloqueia superusuários (devem usar /admin)
    if request.user.is_superuser:
        return redirect('admin:index')

    perfil = getattr(request.user, 'perfil', None)

    # Apenas alunos acessam o portal
    if not perfil or not getattr(perfil, 'aluno', None):
        messages.error(request, "Acesso restrito ao portal de alunos.")
        return redirect('home')

    context = {'perfil': perfil}
    return render(request, 'portal/dashboard.html', context)


# página onde o usuário consegue ver suas respectivas notas

@login_required
def minhas_notas(request):
    perfil = getattr(request.user, 'perfil', None)

    # Sem perfil ou sem aluno: mostra aviso e listas vazias para o template
    if perfil is None or not getattr(perfil, 'aluno', None):
        messages.info(request, "Apenas alunos possuem notas no portal.")
        notas_1bim = Nota1Bim.objects.none()
        notas_2bim = Nota2Bim.objects.none()
        notas_3bim = Nota3Bim.objects.none()
        notas_4bim = Nota4Bim.objects.none()
    else:
        notas_1bim = Nota1Bim.objects.filter(aluno=perfil.aluno)
        notas_2bim = Nota2Bim.objects.filter(aluno=perfil.aluno)
        notas_3bim = Nota3Bim.objects.filter(aluno=perfil.aluno)
        notas_4bim = Nota4Bim.objects.filter(aluno=perfil.aluno)

    bimestres = [
        ('1º Bimestre', notas_1bim),
        ('2º Bimestre', notas_2bim),
        ('3º Bimestre', notas_3bim),
        ('4º Bimestre', notas_4bim),
    ]

    context = {
        'perfil': perfil,
        'bimestres': bimestres,
    }

    return render(request, 'portal/minhas_notas.html', context)


# página onde o usuário vê as informações de pagamento da mensalidade

# function mensalidade(request)
@login_required
def mensalidade(request):
    # Obtém o perfil de forma segura
    perfil = getattr(request.user, 'perfil', None)

    # Sem Perfil: abre a página com listas vazias e um aviso
    if perfil is None:
        messages.info(
            request,
            "Você está logado sem Perfil vinculado. Não há mensalidades para exibir."
        )
        mensalidades = Mensalidade.objects.none()
    else:
        # Aluno: mensalidades do próprio aluno
        if perfil.aluno:
            mensalidades = Mensalidade.objects.filter(aluno=perfil.aluno)
        # Responsável: mensalidades de todos os alunos vinculados
        elif perfil.responsavel:
            mensalidades = Mensalidade.objects.filter(aluno__responsavel=perfil.responsavel)
        # Outros perfis (ex.: professor): nenhuma mensalidade
        else:
            mensalidades = Mensalidade.objects.none()

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

@login_required
def dashboard_professor(request):
    professor = get_object_or_404(Professor, user=request.user)
    turmas = Turma.objects.filter(padrinho_da_turma=professor)

    context = {
        'professor': professor,
        'turmas' : turmas
    }

    return render(request, 'professor/dashboard.html', context)

class ProfessorLoginView(LoginView):
    template_name = 'professor/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard_professor')
    
    # Função de logout no nível do módulo (fora de qualquer classe)
    def logout_view(request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "Você saiu da sua conta com sucesso.")
        return redirect('login')

@login_required
def fazer_chamada(request, turma_id):
    try:
        professor = request.user.professor
    except Professor.DoesNotExist:
        return redirect('home')
    
    turma = get_object_or_404(Turma, id=turma_id)

class PortalLoginView(LoginView):
    template_name = 'portal/seu_login.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        user = self.request.user
        if not user.is_authenticated:
            return resolve_url('login')

        # Superusuário → /admin
        if user.is_superuser:
            return resolve_url('admin:index')

        # Tentar localizar/criar vínculo de Perfil com Aluno
        perfil = getattr(user, 'perfil', None)

        aluno = None
        if getattr(user, 'email', None):
            aluno = Aluno.objects.filter(email__iexact=user.email).first()
        if aluno is None:
            aluno = Aluno.objects.filter(email__iexact=user.username).first()

        if aluno:
            if perfil is None:
                perfil = Perfil.objects.create(user=user, aluno=aluno)
            elif getattr(perfil, 'aluno', None) is None:
                perfil.aluno = aluno
                perfil.save()

        # Aluno vinculado → /portal
        if perfil and getattr(perfil, 'aluno', None):
            return resolve_url('dashboard')

        # Sem perfil ou sem aluno → home
        return resolve_url('home')
    
    # Função de logout no nível do módulo (fora de qualquer classe)
    def logout_view(request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "Você saiu da sua conta com sucesso.")
        return redirect('login')
    
    
