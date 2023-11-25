from django.contrib import admin
from evotar.models import Eleitor, Candidato

@admin.register(Eleitor)
class EleitorAdmin(admin.ModelAdmin):
    list_display = ['matricula', 'cpf', 'name', 'token_valid_vote', 'date_exp_valid_vote', 'token_resetpassword', 'date_token_resetpassword']
    search_fields = ['matricula', 'cpf', 'name']
    list_filter = ['groups', 'user_permissions']

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ['matricula', 'cpf', 'name', 'foto_perfil']
    search_fields = ['matricula', 'cpf', 'name']
