from django.db import models
from django.forms import ValidationError

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
        


class Responsavel(models.Model):
    nome_completo_responsavel = models.CharField(max_length=100, verbose_name='Nome Completo')
    email_responsavel = models.EmailField(max_length=50, verbose_name='Email')
    nascimento_responsavel = models.DateField(verbose_name='Data de Nascimento')
    numero_responsavel = models.CharField(max_length=11, verbose_name='Número de telefone')
    cpf_responsavel = models.CharField(max_length=11, unique=True, validators=[validate_cpf], null=True, blank=False)

    def __str__(self):
        return self.nome_completo_responsavel


class Aluno(models.Model):
    nome_completo = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    data_de_nascimento = models.DateField()
    numero_telefone = models.CharField(max_length=11, verbose_name="Insira o número de telefone")
    cpf_aluno = models.CharField(max_length=11, unique=True, validators=[validate_cpf])
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name='alunos', verbose_name="Responsável")

    def __str__(self):
        return f"{self.nome_completo} {self.responsavel}"


class Professor(models.Model):
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
