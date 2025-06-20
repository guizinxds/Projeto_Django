from django.contrib import admin
from secretaria.models import *

from django.forms.models import BaseInlineFormSet


class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'email', 'data_de_nascimento','numero_telefone', 'cpf_aluno', 'contrato_pdf_link')
    list_display_links = ('nome_completo', 'email', 'numero_telefone')
    search_fields = ('nome_completo',)
    change_list_template = "admin/secretaria/aluno/change_list.html"

 # BOTÃO QUE GERA O PDF DO CONTRATO ESCOLAR
    def contrato_pdf_link(self, obj):
        if obj.responsavel:
            url = reverse('contrato_pdf', args=[obj.id, obj.responsavel.id])
            return format_html('<a class="button" href="{}" target="_blank">Gerar Contrato PDF</a>', url)

    contrato_pdf_link.short_description = 'Contrato PDF'
    

class ResponsavelAdmin(admin.ModelAdmin):
   list_display = ('nome_completo_responsavel','email_responsavel', 'nascimento_responsavel', 'numero_responsavel', 'cpf_responsavel')
   list_display_links = ('nome_completo_responsavel','email_responsavel', 'numero_responsavel')
   search_fields = ('nome_completo_responsavel',)

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome_completo_professor','email_professor', 'nascimento_professor', 'numero_professor', 'cpf_professor')
    list_display_links = ('nome_completo_professor','email_professor', 'numero_professor')
    search_fields = ('nome_completo_professor',)



class NotaInlineFormSet(BaseInlineFormSet):
    
        # GARENTE QUE AS NOTAS EXISTENTES SEJAM CARREGADAS CORRETAMENTE
    def get_queryset(self):
        return super().get_queryset().select_related('aluno')


        # GARANTE QUE OS ALUSO DA TURMA QUE AINDA NÃO TEM NOTA APAREÃM COMO NOVOS FURMULÁRIOS
    def get_initial(self):
        turma = self.instance
        alunos_com_nota = self.get_queryset().values_list("aluno_id", flat=True)
        alunos_sem_nota = Aluno.objects.filter(turma=turma).exclude(id__in=alunos_com_nota)
        return [{'aluno': aluno} for aluno in alunos_sem_nota]


        # CRIA TANTO FORMULÁRIOS EXTRAS QUANTO ALUNOS QUE AINDA NÃO TEM NOTAS
    def get_extra(self):
        return len(self.get_initial())


class Nota1BimInline(admin.TabularInline):  
    model = Nota1Bim
    extra = 1
    def formfield_for_foreignkey(self, db_field, request = None, **kwargs):
        if db_field.name == "aluno":
            if request.resolver_match:
                turma_id = request.resolver_match.kwargs.get('object_id')
                if turma_id:
                    kwargs['queryset'] = Aluno.objects.filter(turma_id=turma_id)
                else:
                    kwargs['queryset'] = Aluno.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class Nota2BimInline(admin.TabularInline):
    model = Nota2Bim
    extra = 1
    def formfield_for_foreignkey(self, db_field, request = None, **kwargs):
        if db_field.name == "aluno":
            if request.resolver_match:
                turma_id = request.resolver_match.kwargs.get('object_id')
                if turma_id:
                    kwargs['queryset'] = Aluno.objects.filter(turma_id=turma_id)
                else:
                    kwargs['queryset'] = Aluno.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class Nota3BimInline(admin.TabularInline):
    model = Nota3Bim
    extra = 1
    def formfield_for_foreignkey(self, db_field, request = None, **kwargs):
        if db_field.name == "aluno":
            if request.resolver_match:
                turma_id = request.resolver_match.kwargs.get('object_id')
                if turma_id:
                    kwargs['queryset'] = Aluno.objects.filter(turma_id=turma_id)
                else:
                    kwargs['queryset'] = Aluno.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class Nota4BimInline(admin.TabularInline):
    model = Nota4Bim
    extra = 1
    def formfield_for_foreignkey(self, db_field, request = None, **kwargs):
        if db_field.name == "aluno":
            if request.resolver_match:
                turma_id = request.resolver_match.kwargs.get('object_id')
                if turma_id:
                    kwargs['queryset'] = Aluno.objects.filter(turma_id=turma_id)
                else:
                    kwargs['queryset'] = Aluno.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('escolha_a_turma','descricao_da_turma', 'padrinho_da_turma','link_para_notas',)
    list_display_links = ('escolha_a_turma','descricao_da_turma', 'padrinho_da_turma')
    search_fields = ('escolha_a_turma',)

    inlines = [Nota1BimInline, Nota2BimInline, Nota3BimInline, Nota4BimInline]

class MateriaAdmin(admin.ModelAdmin):
    list_display = ("id", "matter_choices",)
    list_display_links = ("matter_choices",)
    search_fields = ("matter_choices",)
    list_filter = ("matter_choices",)

class PerfilAdmin(admin.ModelAdmin):
    list_display = ["user", "aluno", "responsavel"]
    readonly_fields = ('responsavel',)

class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'data', 'horario', 'publico_alvo',)
    list_display_links = ('titulo', 'descricao', 'data',)
    search_fields = ('titulo',)

class MensalidadeAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'mes_referente', 'valor', 'pago', 'data_pagamento',)
    list_display_links = ('aluno', 'pago', 'data_pagamento',)
    search_fields = ('aluno',)

admin.site.register(Mensalidade, MensalidadeAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Turma,TurmaAdmin)
admin.site.register(Responsavel,ResponsavelAdmin)
admin.site.register(Aluno,AlunoAdmin)
admin.site.register(Professor,ProfessorAdmin)   
admin.site.register(Materia,MateriaAdmin)