from django.core.mail import send_mail
from django.conf import settings
import random
import string


# Verifica se o admin esta autenticado
def is_admin(user):
    return user.is_authenticated and user.is_superuser

def gerar_token():
    # Gera 4 números aleatórios
    numeros = ''.join(random.choices(string.digits, k=4))

    # Gera 2 letras aleatórias
    letras = ''.join(random.choices(string.ascii_letters, k=2))

    # Combina os números e letras em ordem aleatória
    token = ''.join(random.sample(numeros + letras, len(numeros + letras)))

    return token


def enviar_token_email(user, token):
    # Configura o e-mail
    assunto = 'Redefinição de Senha E-Votos'
    mensagem = f'Olá {user.name},\n\nEste é seu token para redefinir sua senha: {token}.\nEle tem validade de apenas 5 minutos!'
    remetente = f'{settings.EMAIL_HOST_USER}'  # Substitua pelo seu endereço de e-mail

    # Envia o e-mail
    send_mail(
        assunto,
        mensagem,
        remetente,
        [user.email],
        fail_silently=False,
    )
