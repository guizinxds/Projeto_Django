from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Importa as views do seu app secretaria
from secretaria import views

# Importa apenas a view de refresh, pois a de obter token agora é a nossa customizada
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # SUAS URLS ORIGINAIS (para o site renderizado pelo Django)
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('contrato/pdf/<int:aluno_id>/<int:responsavel_id>/', views.ContratoAlunosPdfView.as_view(), name='contrato_pdf'),
    path('notas/', views.notas_por_bimestre, name='notas_por_bimestre'),
    path('portal/', views.dashboard, name='dashboard'),
    path('portal/notas/', views.minhas_notas, name='minhas_notas'),
    path('portal/mensalidades/', views.mensalidade, name='minhas_mensalidades'),
    path('portal/eventos/', views.eventos, name='eventos'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='portal/seu_login.html'), name='login'),
    path('mensalidade/pdf/<int:mensalidade_id>/',  views.gerar_boleto, name='gerar_boleto'),

    # --- NOSSAS URLS DE API PARA O FRONT-END REACT ---
    path('api/alunos/', views.api_listar_alunos, name='api_listar_alunos'),

    # --- URLS DE AUTENTICAÇÃO E TOKEN ---
    # Esta linha foi ATUALIZADA para usar a nossa view customizada (MyTokenObtainPairView)
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Esta linha permanece a mesma, usando a view padrão da biblioteca
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Configuração para servir arquivos de mídia em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)