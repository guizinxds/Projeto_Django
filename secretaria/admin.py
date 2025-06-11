from django.contrib import admin
from secretaria.models import *

from django.forms.models import BaseInlineFormSet


class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'email', 'data_de_nascimento','numero_telefone', 'cpf_aluno', 'contrato_pdf_link')
    list_display_links = ('nome_completo', 'email', 'numero_telefone')
    search_fields = ('nome_completo',)

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
    def get_queryset(self):
        # Garante que notas existentes sejam carregadas corretamente
        return super().get_queryset().select_related('aluno')

    def get_initial(self):
        # Garante que os alunos da turma que ainda não têm nota apareçam como novos formulários
        turma = self.instance
        alunos_com_nota = self.get_queryset().values_list("aluno_id", flat=True)
        alunos_sem_nota = Aluno.objects.filter(turma=turma).exclude(id__in=alunos_com_nota)
        return [{'aluno': aluno} for aluno in alunos_sem_nota]

    def get_extra(self):
        # Cria tantos formulários extras quanto alunos ainda não têm notas
        return len(self.get_initial())


class NotaInline(admin.TabularInline):
    model = Nota
    # formset = NotaInlineFormSet
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
    
    # fields = ('aluno', 'materia', 'nota1bim', 'nota2bim','nota3bim', 'nota4bim', 'media_final')
    # readonly_fields = ('aluno',) #impede que o nome do aluno seja alterado no admin

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('escolha_a_turma','descricao_da_turma', 'padrinho_da_turma')
    list_display_links = ('escolha_a_turma','descricao_da_turma', 'padrinho_da_turma')
    search_fields = ('escolha_a_turma',)

    inlines = [NotaInline]

class MateriaAdmin(admin.ModelAdmin):
    list_display = ("id", "matter_choices",)
    list_display_links = ("matter_choices",)
    search_fields = ("matter_choices",)
    list_filter = ("matter_choices",)


admin.site.register(Turma,TurmaAdmin)
admin.site.register(Responsavel,ResponsavelAdmin)
admin.site.register(Aluno,AlunoAdmin)
admin.site.register(Professor,ProfessorAdmin)   
admin.site.register(Materia,MateriaAdmin)



