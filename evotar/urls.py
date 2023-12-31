from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from evotar.views import (
    index, adm_home, 
    login_view, logout_view,
    recuperar_senha, redefinir_senha,
    cadastro_eleitor, cadastro_candidato,
    nova_eleicao, eleicao, editar_candidatos_todos,
    editar_candidato, editar_eleitores_todos, editar_eleitor,
    editar_eleicao_todos, editar_eleicao
)

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('index/', index, name='index'),
    path('adm-home/', adm_home, name='adm_home'),

    path('cadastro-eleitor/', cadastro_eleitor, name='cadastro_eleitor'),
    path('editar-eleitores-todos/', editar_eleitores_todos, name='editar_eleitores_todos'),
    path('editar_eleitor/<int:eleitor_id>', editar_eleitor, name='editar_eleitor'),
    
    path('cadastro-candidato/', cadastro_candidato, name='cadastro_candidato'),
    path('editar-candidatos-todos/', editar_candidatos_todos, name='editar_candidatos_todos'),
    path('editar-candidato/<int:candidato_id>', editar_candidato, name='editar_candidato'),

    path('adm-home/nova-eleicao/', nova_eleicao, name='nova_eleicao'),
    path('adm-home/editar-eleicao/', editar_eleicao_todos, name='editar_eleicao_todos'),
    path('editar-eleicao/<int:eleicao_id>', editar_eleicao, name='editar_eleicao'),

    
    path('recuperar-senha/', recuperar_senha, name='recuperar_senha'),

    # URL para a página de redefinição de senha com token
    path('redefinir-senha/', redefinir_senha, name='redefinir_senha'),

    path('index/eleicao/', eleicao, name='eleicao'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# As seguintes linhas são para servir os arquivos de mídia durante o desenvolvimento:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)