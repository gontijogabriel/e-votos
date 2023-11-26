from django.contrib import admin
from evotar.models import Candidato, Eleitor, Eleicao, Voto

@admin.register(Eleitor)
class EleitorAdmin(admin.ModelAdmin):
    list_display = ['matricula','email', 'cpf', 'name', 'token_valid_vote', 'date_exp_valid_vote', 'token_resetpassword', 'date_token_resetpassword']
    search_fields = ['matricula', 'cpf', 'name']
    list_filter = ['groups', 'user_permissions']

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ['matricula', 'cpf', 'nome', 'foto_perfil']
    search_fields = ['matricula', 'cpf', 'nome']

@admin.register(Eleicao)
class EleicaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'data_inicio', 'data_fim')
    filter_horizontal = ('candidatos',)

@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    list_display = ('eleitor', 'eleicao', 'candidato_escolhido')