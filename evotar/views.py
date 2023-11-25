from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login # Função renomeada para evitar conflito
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                # O usuário é um admin!
                print('O usuário é um admin!')
                auth_login(request, user)
                return redirect('adm_home')
            else:
                # O usuário não é um admin!
                print('Você não tem permissão de admin!')
                auth_login(request, user)
                return redirect('index')
        else:
            print('Credenciais inválidas')

    return render(request, 'login.html')

# Cadastro
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
