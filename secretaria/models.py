from django.db import models
from django.forms import ValidationError

from django.utils.html import format_html
from django.urls import reverse

import re


def validate_cpf(value):
    cpf = [int(char) for char in value if char.isdigit()]
    if len(cpf) != 11 or len(set(cpf)) == 1:
        raise ValidationError("CPF inválido.")
    
    for i in range(9, 11):
        value_sum = sum(cpf[num] * ((i + 1) - num) for num in range(0, i))
        digit = (value_sum * 10 % 11) % 10
        if digit != cpf[i]:
            raise ValidationError("CPF inválido.")
        
def validate_nota(value):
    if not (0 <= value <= 10):
        raise ValidationError(
            f"Nota inválida: {value}. A nota deve estar entre 0 e 10."
        )
        


class Responsavel(models.Model):
    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"

    nome_completo_responsavel = models.CharField(max_length=100, verbose_name='Nome Completo')
    email_responsavel = models.EmailField(max_length=50, verbose_name='Email')
    nascimento_responsavel = models.DateField(verbose_name='Data de Nascimento')
    numero_responsavel = models.CharField(max_length=11, verbose_name='Número de telefone')
    cpf_responsavel = models.CharField(max_length=11, unique=True, validators=[validate_cpf], null=True, blank=False)

    def __str__(self):
        return self.nome_completo_responsavel


class Aluno(models.Model):
    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    nome_completo = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    data_de_nascimento = models.DateField()
    numero_telefone = models.CharField(max_length=11, verbose_name="Insira o número de telefone")
    cpf_aluno = models.CharField(max_length=11, unique=True, validators=[validate_cpf])
    responsavel = models.ForeignKey(
        'Responsavel',
        on_delete=models.CASCADE,
        related_name='alunos',
        verbose_name="Responsável"
    )

    #Campo para anexar PDF
    documento_pdf = models.FileField(
        upload_to='documentos_alunos/',
        null=True,
        blank=True,
        verbose_name="Anexar Contrato PDF"
    )

    def __str__(self):
        return self.nome_completo

    # def __str__(self):
    #     return f"{self.nome_completo} {self.responsavel}"
    
    # def contrato_pdf_link(self):
    #     url = reverse('contrato_pdf', args=[self.id])
    #     return format_html('<a class="button" href="{}" target="_blank"> Gerar contrato PDF</a>', url)
    
    #     contrato_pdf_link.short_description = "Contrato em PDF"


class Professor(models.Model):
    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    nome_completo_professor = models.CharField(max_length=100, verbose_name='Nome Completo')
    email_professor = models.EmailField(max_length=50, verbose_name='Email')
    nascimento_professor = models.DateField(verbose_name='Data de Nascimento')
    numero_professor = models.CharField(max_length=11, verbose_name='Número de telefone')
    cpf_professor = models.CharField(max_length=11, unique=True, validators=[validate_cpf])

    def __str__(self):
        return self.nome_completo_professor

           
class Turma(models.Model):
    ITINERARIO_CHOICES = (
        ('JG', 'JOGOS DIGITAIS'),
        ('CN', 'CIÊNCIAS DA NATUREZA'),
        ('DS', 'DESENVOLVIMENTO DE SISTEMAS'),
        ('RS', 'REDES DE COMPUTADORES'),
    )

    TURMA_CHOICES = (
        ('1A', '1 ANO A'),
        ('1B', '1 ANO B'),
        ('1C', '1 ANO C'),
        ('2A', '2 ANO A'),
        ('2B', '2 ANO B'),
        ('2C', '2 ANO C'),
        ('3A', '3 ANO A'),
        ('3B', '3 ANO B'),
        ('3C', '3 ANO C'),
    )

    escolha_a_turma = models.CharField(max_length=2, choices=TURMA_CHOICES, blank=True, null=False)
    descricao_da_turma = models.CharField(max_length=2, choices=ITINERARIO_CHOICES, verbose_name='Informe o Itinerário da Turma')
    padrinho_da_turma = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='turmas', verbose_name='Padrinho da Turma', null=True, blank=False)

    def __str__(self):
        return f"{self.escolha_a_turma} {self.padrinho_da_turma}"
    
class Materia(models.Model):
   
        MATTER_CHOICES = (
        ("CH", "Ciencias Humanas"),
        ("L", "Linguagens"),
        ("M", "Matematica"),
        ("CN", "Ciencias da Natureza"),
    )
        matter_choices = models.CharField(max_length=50, choices=MATTER_CHOICES , blank=False, null=True,)

        def _str_(self):
            return f"{self.get_matter_choices_display()}"
