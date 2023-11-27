from django.contrib.auth.models import AbstractUser
from django.db import models


class Eleitor(AbstractUser):
    matricula = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=255)

    token_valid = models.CharField(max_length=255, blank=True, null=True)
    date_token = models.CharField(max_length=255, blank=True, null=True)

    groups = models.ManyToManyField('auth.Group', related_name='eleitor_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='eleitor_user_permissions', blank=True)

    def __str__(self):
        return self.username

    
class Candidato(models.Model):
    nome = models.CharField(max_length=255)
    matricula = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)

    def __str__(self):
        return self.matricula

class Eleicao(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    candidatos = models.ManyToManyField(Candidato, related_name='eleicoes')
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    def __str__(self):
        return self.nome

class Voto(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.CASCADE)
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE)
    candidato_escolhido = models.ForeignKey(Candidato, on_delete=models.CASCADE)