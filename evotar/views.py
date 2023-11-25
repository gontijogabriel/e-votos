from django.shortcuts import render, redirect
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login # Função renomeada para evitar conflito
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from evotar.utils import enviar_token_email, gerar_token
from django.conf import settings

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                # O usuário é um admin!
                auth_login(request, user)
                return redirect('adm_home', user)
            else:
                # O usuário não tem permissão de admin!
                auth_login(request, user)
                return redirect('index')
        else:
            return render(request, 'login.html', {'erro': 'Credenciais inválidas'})

    return render(request, 'login.html')

# Cadastro de Eleitor
def cadastro_eleitor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        matricula = request.POST.get('matricula')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        password1 = request.POST.get('password-1')
        password2 = request.POST.get('password-2')

        if password1 == password2:
            User = get_user_model()
            User.objects.create_user(username=email, email=email, password=password1, name=name, matricula=matricula, cpf=cpf)
            return redirect('login')
        else:
            print('As senhas não coincidem')

    return render(request, 'cadastro_eleitor.html')

# Recuperacao de Senha
def recuperar_senha(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            User = get_user_model()
            user = User.objects.get(email=email)

            token = gerar_token()

            # Armazena o token no banco de dados associado ao usuário
            user.token_resetpassword = token
            user.date_token_resetpassword = datetime.now()
            user.save()

            # manda email con token
            # enviar_token_email(user, token)

            try:
                enviar_token_email(user, token)
            except:
                print('erro ao mandar email com token')
            
            return render(request, 'token_recuperar_senha.html', {'email_user': email})

        except User.DoesNotExist:
            print('Usuário não encontrado, continue com o processo de cadastro')
            return render(request, 'login.html')

    return render(request, 'recuperar_senha.html')

# Redefinir Senha
def redefinir_senha(request):
    if request.method == 'POST':
        email = request.POST.get('email_user')
        token = request.POST.get('token')
        senha1 = request.POST.get('password-1')
        senha2 = request.POST.get('password-2')

        # Obtenha o usuário com base no e-mail
        User = get_user_model()
        user = User.objects.get(email=email)

        print(f'TEMPO EM SEGUNDOS DA VALIDADE DO TOKEN = {settings.TOKEN_TIME_TO_DIE}')

        # Verifique se o token é válido e se não expirou
        if user.token_resetpassword == token and user.date_token_resetpassword is not None and (datetime.now() - user.date_token_resetpassword).total_seconds() < settings.TOKEN_TIME_TO_DIE: # 5 minutos
            # Verifique se as senhas são iguais
            if senha1 == senha2:
                # Atualize a senha do usuário
                user.set_password(senha1)
                user.save()

                # Limpe o token e a data associada
                user.token_resetpassword = None
                user.date_token_resetpassword = None
                user.save()

                # Redirecione para uma página de sucesso ou faça o que for necessário
                return render(request, 'login.html')

            else:
                # Senhas não coincidem, retorne uma mensagem de erro
                return render(request, 'recuperar_senha.html', {'erro': 'As senhas não coincidem'})

        else:
            # Token inválido ou expirado, retorne uma mensagem de erro
            return render(request, 'recuperar_senha.html', {'erro': 'Token inválido ou expirado'})
            
    return redirect('login')

# Verifica se o admin esta autenticado
def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='index')
def cadastro_candidato(request):
    return render(request, 'cadastro_candidato.html')

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='index')
def adm_home(request):
    return render(request, 'adm_home.html')

def logout_view(request):
    logout(request)
    return redirect('login')
