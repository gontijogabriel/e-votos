# evotar urls.py
from django.urls import path
from evotar.views import index, login_view, logout_view, adm_home, cadastro_eleitor, cadastro_candidato, recuperar_senha, redefinir_senha

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('index/', index, name='index'),
    path('adm_home/', adm_home, name='adm_home'),

    path('cadastro_eleitor/', cadastro_eleitor, name='cadastro_eleitor'),
    path('cadastro_candidato/', cadastro_candidato, name='cadastro_candidato'),

    # path('recuperar_senha/', recuperar_senha, name='recuperar_senha'),
    # path('token_recuperar_senha/', token_recuperar_senha, name='token_recuperar_senha'),
    
    # URL para a página de solicitação de recuperação de senha
    path('recuperar-senha/', recuperar_senha, name='recuperar_senha'),

    # URL para a página de redefinição de senha com token
    path('redefinir-senha/', redefinir_senha, name='redefinir_senha'),
]

# As seguintes linhas são para servir os arquivos de mídia durante o desenvolvimento:
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)