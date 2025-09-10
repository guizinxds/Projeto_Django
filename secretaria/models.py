from django.db import models
from django.forms import ValidationError
from django.utils import timezone

from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import User

import re

# VALIDADOR DE CPF
def validate_cpf(value):
    cpf = [int(char) for char in value if char.isdigit()]
    if len(cpf) != 11 or len(set(cpf)) == 1:
        raise ValidationError("CPF inválido.")
    
    for i in range(9, 11):
        value_sum = sum(cpf[num] * ((i + 1) - num) for num in range(0, i))
        digit = (value_sum * 10 % 11) % 10
        if digit != cpf[i]:
            raise ValidationError("CPF inválido.")


# VALIDADOR DE NOTAS    
def validate_nota(value):
    if not (0 <= value <= 10):
        raise ValidationError(
            f"Nota inválida: {value}. A nota deve estar entre 0 e 10."
        )
        

# MODEL DOS RESPONSÁVEIS
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

# MODEL DOS ALUNOS
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
        verbose_name="Responsável")
    turma = models.ForeignKey("Turma", on_delete=models.CASCADE, related_name='alunos', verbose_name="Turma", null=True, blank=True)

    #CAMPO PARA ANEXAR PDF
    documento_pdf = models.FileField(
        upload_to='documentos_alunos/',
        null=True,
        blank=True,
        verbose_name="Anexar Contrato PDF"
    )

    def __str__(self):
        return self.nome_completo

# MODELS DOS PROFESSORES
class Professor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
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

# MODELS DAS TURMAS
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
        return self.escolha_a_turma


    # BOTÃO CRIADO PARA ACESSAR A PÁGINA DE NOTAS DAS TURMAS
    def link_para_notas(self):

        url = reverse('notas_por_bimestre') + f'?turma={self.escolha_a_turma}'
        

        return format_html('<a class="button" href="{}" target="_blank">Ver Notas</a>', url)
    
    link_para_notas.short_description = "Acessar Notas" 
    link_para_notas.allow_tags = True 


# MODELS DAS MATERIAS   
class Materia(models.Model):
   
        MATTER_CHOICES = (
        ("CH", "Ciencias Humanas"),
        ("L", "Linguagens"),
        ("M", "Matematica"),
        ("CN", "Ciencias da Natureza"),
    )
        matter_choices = models.CharField(max_length=50, choices=MATTER_CHOICES , blank=False, null=True)
        professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='materias', blank=False, null=True)

        def __str__(self):
            return f"{self.get_matter_choices_display()}"

     
# MODELS DAS NOTAS DIVIDIDAS POR BIMESTRE    
class Nota1Bim(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas_1bim', verbose_name='Aluno')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='notas_1bim', verbose_name='Turma') 
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='notas_1bim', verbose_name='Matéria')
    atividade1 = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Atividade1', null=True, blank=True)
    atividade2 = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Atividade2', null=True, blank=True)
    simulado = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Simulado', null=True, blank=True)
    prova = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Prova', null=True, blank=True)

    media_final = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Média Final', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.media_final = (self.atividade1 + self.atividade2 + self.simulado + self.prova) / 4
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.aluno.nome_completo} - {self.turma.escolha_a_turma} - {self.materia.get_matter_choices_display()} - {self.media_final}'
    
class Nota2Bim(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas_2bim', verbose_name='Aluno')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='notas_2bim', verbose_name='Turma') 
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='notas_2bim', verbose_name='Matéria')
    atividade1 = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Atividade1', null=True, blank=True)
    atividade2 = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Atividade2', null=True, blank=True)
    simulado = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Simulado', null=True, blank=True)
    prova = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Prova', null=True, blank=True)

    media_final = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Média Final', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.media_final = (self.atividade1 + self.atividade2 + self.simulado + self.prova) / 4
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.aluno.nome_completo} - {self.turma.escolha_a_turma} - {self.materia.get_matter_choices_display()} - {self.media_final}'
    
class Nota3Bim(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas_3bim', verbose_name='Aluno')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='notas_3bim', verbose_name='Turma') 
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='notas_3bim', verbose_name='Matéria')
    atividade1 = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Atividade1', null=True, blank=True)
    atividade2 = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Atividade2', null=True, blank=True)
    simulado = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Simulado', null=True, blank=True)
    prova = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Prova', null=True, blank=True)

    media_final = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Média Final', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.media_final = (self.atividade1 + self.atividade2 + self.simulado + self.prova) / 4
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.aluno.nome_completo} - {self.turma.escolha_a_turma} - {self.materia.get_matter_choices_display()} - {self.media_final}'
    
class Nota4Bim(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas_4bim', verbose_name='Aluno')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='notas_4bim', verbose_name='Turma') 
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='notas_4bim', verbose_name='Matéria')
    atividade1 = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Atividade1', null=True, blank=True)
    atividade2 = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Atividade2', null=True, blank=True)
    simulado = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Simulado', null=True, blank=True)
    prova = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Prova', null=True, blank=True)

    media_final = models.DecimalField(max_digits=5, decimal_places=1, validators=[validate_nota], verbose_name='Média Final', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.media_final = (self.atividade1 + self.atividade2 + self.simulado + self.prova) / 4
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.aluno.nome_completo} - {self.turma.escolha_a_turma} - {self.materia.get_matter_choices_display()} - {self.media_final}'
    

# MODEL DOS EVENTOS
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateField()   
    horario = models.TimeField()
    publico_alvo = models.CharField(
        max_length=20,
        choices=[
            ('todos','Todos'),('alunos','Alunos'),('reponsaveis','Responsáveis')],
            default = 'todos'
    )

    def __str__(self):
        return f"{self.titulo} - {self.data}"


# MODEL DAS MENSALIDADES
class Mensalidade(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='mensalidades')
    mes_referente = models.CharField(max_length=20,
    choices=[
        ('Janeiro','Janeiro'),('Fevereiro','Fevereiro'),('Março','Março'),('Abril','Abril'),('Maio','Maio'),('Junho','Junho'),('Julho','Julho'),('Agosto','Agosto'),('Setembro','Setembro'),('Outubro','Outubro'),('Novembro','Novembro'),('Dezembro','Dezembro')
    ],
        default = '-----') 
    valor = models.DecimalField(max_digits=7, decimal_places=2)
    pago = models.BooleanField(default=False)
    data_pagamento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.aluno.nome_completo} - {self.mes_referente} - {'Pago' if self.pago else 'Pagamento Pendente'}"
    
# MODEL DOS PERFIS
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, null=True, blank=True)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, null=True, blank=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)

class Aula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now, verbose_name="Data da Aula")
    assunto = models.CharField(max_length=200, blank=True, null=True, verbose_name="Assunto da Aula")

    class Meta:
        unique_together = ('turma', 'data')
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"

    def __str__(self):
        return f"Aula de {self.turma.escolha_a_turma} em {self.data.strftime('%d/%m/%Y')}"

# MODELO DE PRESENÇA
class Presenca(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    presente = models.BooleanField(default=False)

    class Meta: 
        unique_together = ('aluno', 'aula')
        verbose_name = "Presença"
        verbose_name_plural = "Presenças"

    def __str__(self):
        status = "Presente" if self.presente else "Faltou"
        return f"{self.aluno.nome_completo} - {status} em {self.aula.data.strftime('%d/%m/%Y')}"

# NAO PERMITE QUE O RESPONSÁVEL DO PERFIL SEJA ALTERADO, POIS ESTA PEGANDO AS INFORMAÇÕES DO ALUNO SELECIONADO, ASSIM RECEBENDO O RESPONSÁVEL AUTOMATICAMENTE
    # O método save e __str__ abaixo pertencem ao modelo Perfil, não Aula