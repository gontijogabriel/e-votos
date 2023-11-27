from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from evotar.views import (
    index, adm_home, 
    login_view, logout_view,
    recuperar_senha, redefinir_senha,
    cadastro_eleitor, cadastro_candidato,
    nova_eleicao, eleicao
)

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('index/', index, name='index'),
    path('adm-home/', adm_home, name='adm_home'),

    path('cadastro-eleitor/', cadastro_eleitor, name='cadastro_eleitor'),
    path('cadastro-candidato/', cadastro_candidato, name='cadastro_candidato'),

    path('nova-eleicao/', nova_eleicao, name='nova_eleicao'),
    # path('token_recuperar_senha/', token_recuperar_senha, name='token_recuperar_senha'),
    
    # URL para a página de solicitação de recuperação de senha
    path('recuperar-senha/', recuperar_senha, name='recuperar_senha'),

    # URL para a página de redefinição de senha com token
    path('redefinir-senha/', redefinir_senha, name='redefinir_senha'),

    # URL para a página de eleicao
    path('eleicao/', eleicao, name='eleicao'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# As seguintes linhas são para servir os arquivos de mídia durante o desenvolvimento:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)