# evotar urls.py
from django.urls import path
from evotar.views import index, login_view, logout_view, adm_home, cadastro_eleitor, cadastro_candidato

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('index/', index, name='index'),
    path('adm_home/', adm_home, name='adm_home'),
    path('cadastro_eleitor', cadastro_eleitor, name='cadastro_eleitor'),
    path('cadastro_candidato/', cadastro_candidato, name='cadastro_candidato'),
]