
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from secretaria import views

urlpatterns = [
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
    path('mensalidade/pdf/<int:mensalidade_id>/',  views.gerar_boleto, name='gerar_boleto')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)