
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from secretaria import views

urlpatterns = [
    path('admin/', admin.site.urls),
          
    path('contrato/pdf/<int:aluno_id>/<int:responsavel_id>/', views.ContratoAlunosPdfView.as_view(), name='contrato_pdf'),

    path('notas/', views.notas_por_bimestre, name='notas_por_bimestre'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)