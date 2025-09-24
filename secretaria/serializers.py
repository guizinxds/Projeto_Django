#thiago 24/09

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Perfil

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Chama o método original para obter o token básico
        token = super().get_token(user)

        # Adiciona nossos dados customizados ("claims") ao token
        token['username'] = user.username
        
        # Tenta encontrar o perfil do usuário para adicionar o tipo
        try:
            perfil = user.perfil
            if perfil.aluno:
                token['profile_type'] = 'aluno'
                token['aluno_id'] = perfil.aluno.id
            elif perfil.professor:
                # Agrupando professor como um "trabalhador"
                token['profile_type'] = 'trabalhador'
                token['professor_id'] = perfil.professor.id
            # Você pode adicionar um `elif perfil.responsavel:` aqui se necessário
            else:
                token['profile_type'] = 'desconhecido'
        except Perfil.DoesNotExist:
            token['profile_type'] = 'sem_perfil'

        return token