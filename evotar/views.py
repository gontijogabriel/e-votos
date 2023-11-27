from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login # Função renomeada para evitar conflito
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from evotar.utils import is_admin, enviar_token_email, gerar_token
from django.conf import settings
from evotar.models import Eleicao, Candidato

# Login
def login_view(request):
    logout(request)

    msg = ''

    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                # O usuário é um admin!
                auth_login(request, user)
                return redirect('adm_home')
            else:
                # O usuário não tem permissão de admin!
                auth_login(request, user)
                return redirect('index')
        else:
            msg = 'Credenciais inválidas'
            
    return render(request, 'login.html', {'msg': msg}) 

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
    msg = ''
    
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            User = get_user_model()
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                msg = 'Usuário não cadastrado com esse email'
                return render(request, 'recuperar_senha.html', {'msg': msg})
            
            token = str(gerar_token())

            print(token)
            
            user.token_valid = token
            user.date_token = datetime.now()
            user.save()

            try:
                enviar_token_email(user, token)
                
                return render(request, 'token_recuperar_senha.html', {'email_user': email})
            
            except Exception as e:
                print(f'Erro ao mandar email com token: {e}')
                msg = 'Erro ao enviar o email com o token'
            
            return render(request, 'recuperar_senha.html', {'msg': msg})

        except User.DoesNotExist:
            print('Usuário não encontrado, continue com o processo de cadastro')
            msg = 'Usuário não encontrado'
            return render(request, 'login.html', {'msg': msg})

    return render(request, 'recuperar_senha.html', {'msg': msg})

# Redefinir Senha
def redefinir_senha(request):
    msg = request.GET.get('msg', '')
    
    if request.method == 'POST':
        email = request.POST.get('email_user')
        token = request.POST.get('token')
        senha1 = request.POST.get('password-1')
        senha2 = request.POST.get('password-2')

        User = get_user_model()
        user = User.objects.get(email=email)

        # Verifique se o token é válido e se não expirou
        if user.token_resetpassword == token and user.date_token_resetpassword is not None: # and (datetime.now() - user.date_token_resetpassword).total_seconds() < settings.TOKEN_TIME_TO_DIE: # 5 minutos
            # Verifique se as senhas são iguais
            if senha1 == senha2:
                # Atualize a senha do usuário
                user.set_password(senha1)
                user.save()

                # Limpe o token e a data associada
                user.token_resetpassword = None
                user.date_token_resetpassword = None
                user.save()

        # Valida se o email existe antes de tentar recuperar o usuário
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            msg = 'Usuário não encontrado'
            return render(request, 'token_recuperar_senha.html', {'msg': msg})
        
        formato_string = "%Y-%m-%d %H:%M:%S.%f"
        date_token_dt = datetime.strptime(user.date_token, formato_string)
        vida_token = datetime.now() - date_token_dt

        try:
            if user.token_valid == token:

                if vida_token.seconds < settings.TOKEN_TIME_TO_DIE:

                    if senha1 == senha2:
                        # Atualize a senha do usuário
                        user.set_password(senha1)
                        user.save()
                        print('----- 6 -----')
                        # Limpe o token e a data associada
                        user.token_resetpassword = None
                        user.date_token_resetpassword = None
                        user.save()
                        print('----- 7 -----')
                        return render(request, 'login.html')
                    else:
                        msg = 'As senhas não coincidem'
                else:
                    msg = 'Tempo de vida do Token expirado!'
            else:
                msg = 'Token incorreto'
        except Exception as e:
            print(f'Erro "redefinir_senha": {e}')
            msg = 'Erro durante a redefinição da senha'

    return render(request, 'token_recuperar_senha.html', {'msg': msg, 'email_user': email})


@login_required(login_url='login')
def index(request):
    eleicoes = Eleicao.objects.all()
    return render(request, 'index.html', {'eleicoes': eleicoes})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def adm_home(request):
    return render(request, 'adm_home.html')

from django.db import IntegrityError
@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def cadastro_candidato(request):
    msg = request.GET.get('msg', '')
    
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            matricula = request.POST.get('matricula')
            cpf = request.POST.get('cpf')
            foto_perfil = request.FILES.get('foto_perfil')

            if Candidato.objects.filter(cpf=cpf).exists():
                msg = 'Candidato com CPF já cadastrado.'
            else:
                novo_candidato = Candidato(nome=nome, matricula=matricula, cpf=cpf, foto_perfil=foto_perfil)
                novo_candidato.save()
                msg = 'Candidato cadastrado com sucesso!'
        except IntegrityError:
            msg = 'Erro ao cadastrar candidato. CPF já cadastrado.'
    
    return render(request, 'cadastro_candidato.html', {'msg': msg})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def nova_eleicao(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        tipo_de_eleicao = request.POST.get('tipo_de_eleicao')
        data_de_inicio = request.POST.get('data_de_inicio')
        data_de_fim = request.POST.get('data_de_fim')

        candidatos_selecionados = request.POST.getlist('candidatos')

        eleicao = Eleicao.objects.create(
            nome=nome,
            tipo=tipo_de_eleicao,
            data_inicio=data_de_inicio,
            data_fim=data_de_fim
        )

        eleicao.candidatos.set(candidatos_selecionados)

        return render(request, 'adm_home.html')
    
    candidatos = Candidato.objects.all()
    return render(request, 'nova_eleicao.html', {'candidatos': candidatos})



@login_required(login_url='login')
def eleicao(request):
    if request.method == 'POST':
        eleicao_id = request.POST.get('eleicao_id')
        
        # Obtém a eleição com o ID fornecido ou retorna um erro 404 se não existir
        eleicao = get_object_or_404(Eleicao, id=eleicao_id)

        # Obtém todos os candidatos associados a esta eleição
        candidatos = eleicao.candidatos.all()

        # Renderiza o template com os dados
        return render(request, 'eleicao.html', {'eleicao': eleicao, 'candidatos': candidatos})

    eleicoes = Eleicao.objects.all()
    return render(request, 'index.html', {'eleicoes': eleicoes})



def logout_view(request):
    logout(request)
    return redirect('login')
