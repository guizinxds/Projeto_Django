from django.contrib import admin
from secretaria.models import *


class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'email', 'data_de_nascimento','numero_telefone')
    list_display_links = ('nome_completo', 'email', 'numero_telefone')
    search_fields = ('nome_completo',)

class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('nome_completo_responsavel','email_responsavel', 'nascimento_responsavel', 'numero_responsavel')
    list_display_links = ('nome_completo_responsavel','email_responsavel', 'numero_responsavel')
    search_fields = ('nome_completo_responsavel',)

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome_completo_professor','email_professor', 'nascimento_professor', 'numero_professor')
    list_display_links = ('nome_completo_professor','email_professor', 'numero_professor')
    search_fields = ('nome_completo_professor',)

# class TurmaAdmin(admin.ModelAdmin):



admin.site.register(Aluno,AlunoAdmin)
admin.site.register(Responsável,ResponsavelAdmin)
admin.site.register(Professor,ProfessorAdmin)   



