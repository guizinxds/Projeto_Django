from django.db import models

class Aluno(models.Model):
    nome_completo = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    data_de_nascimento = models.DateField()
    numero_telefone = models.CharField(max_length=11,verbose_name="Insira o número de telefone")
    
    def __str__(self):
        return self.nome_completo
    
class Responsável(models.Model):
    nome_completo_responsavel = models.CharField(max_length=100,verbose_name='Nome Completo')
    email_responsavel = models.EmailField(max_length=50, verbose_name='Email')
    nascimento_responsavel = models.DateField(verbose_name='Data de Nascimento')
    numero_responsavel = models.CharField(max_length=11,verbose_name='Número de telefone')

    def __str__(self):
        return self.nome_completo_responsavel
    
class Professor(models.Model):
    nome_completo_professor = models.CharField(max_length=100,verbose_name='Nome Completo')
    email_professor = models.EmailField(max_length=50, verbose_name='Email')
    nascimento_professor = models.DateField(verbose_name='Data de Nascimento')
    numero_professor = models.CharField(max_length=11,verbose_name='Número de telefone')

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
        ('1A', '1 ANO A')
        ('1B', '1 ANO B')
        ('1C', '1 ANO C')
        ('2A', '2 ANO A')
        ('2B', '2 ANO B')
        ('2C', '2 ANO C')
        ('3A', '3 ANO A')
        ('3B', '3 ANO B')
        ('3C', '3 ANO C')
    )

    escolha_a_turma = models.CharField(max_length=2, choices=TURMA_CHOICES,blank=True, null=False)
    descricao_da_turma = models.CharField(max_length=2, choices=ITINERARIO_CHOICES, verbose_name='Informe o Itinerário da Turma')
    padrinho_da_turma = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='turmas',verbose_name='Padrinho da Turma', null=True, blank=False)


    def __str__(self):
        return f"{self.escolha_a_turma} {self.padrinho_da_turma}"