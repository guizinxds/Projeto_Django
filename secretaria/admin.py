from django.contrib import admin
from secretaria.models import *


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

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('escolha_a_turma','descricao_da_turma', 'padrinho_da_turma')
    list_display_links = ('escolha_a_turma','descricao_da_turma', 'padrinho_da_turma')
    search_fields = ('escolha_a_turma',)

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



