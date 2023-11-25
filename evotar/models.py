from django.contrib.auth.models import AbstractUser
from django.db import models

# class CustomUser(AbstractUser):
class Eleitor(AbstractUser):
    matricula = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=255)

    groups = models.ManyToManyField('auth.Group', related_name='eleitor_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='eleitor_user_permissions', blank=True)

    def __str__(self):
        return self.username
    
class Candidato(models.Model):
    matricula = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=255)
    
