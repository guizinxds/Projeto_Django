# Sistema de Secretaria Escolar

Sistema desenvolvido em Django para gestão escolar.

##Tecnologias Utilizadas

- [Python 3.13.3](https://www.python.org/)
- [Django 5.2.3](https://www.djangoproject.com/)
- SQLite (padrão, pode ser adaptado para outros bancos)
- HTML, CSS (com Bootstrap)
- xHtml2Pdf(para geração de PDF)
- Admin Django para gestão interna

##Instalação e Execução

###Pré Requisitos

-Python instalado
-Pip
-Ambiente Virtual


###Passos para rodar o projeto

1.**Clone ou extraia o projeto:**

'''bash
git clone https://github.com/guizinxds/Projeto_Django

ou extraia o arquivo .zip

2.**Acesse a pasta do projeto:**

cd Sistema_Secretaria/Sistema_Secretaria

3.**Crie e ative um ambiente virtual**

python -m venv env
env\Scripts\activate

4. **Instale as dependências necessárias:**

pip install django
pip install xhtml2pdf

5.**Realize as migrações do banco de dados:**

python manage.py makemigrations
python manage.py migrate

6.**Crie um superusuário (administrador):**

python manage.py createsuperuser

7.**Execute o servidor de desenvolvimento:**

python manage.py runserver

8.**Acesse no navegador:**

Admin Django: http://127.0.0.1:8000/admin/


##Funcionalidades do sistema

**Gestão de Alunos**
Cadastro completo de alunos

**Associação de responsáveis**
Visualização de dados do aluno

**Gestão de Professores**
Cadastro de professores
Login diferenciado para professores

**Gestão de Turmas**
Criação e edição de turmas
Associação de alunos às turmas
Visualização de lista de alunos por turma

 **Lançamento de Notas**
Cadastro e edição de notas
Relatórios de desempenho por aluno

 **Geração de Documentos**
Geração de contratos em PDF
Geração de boletos ou comprovantes

 **Eventos e Comunicados**
Cadastro e listagem de eventos escolares

 **Sistema de Login**
Login personalizado para administradores, professores e alunos
