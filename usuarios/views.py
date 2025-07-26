from django.shortcuts import render, redirect
from .forms import FormularioLogin, FormularioCadastro
from .models import Usuario

def login(request):
    """View que retornará a página de login da calculadora"""
    return render(request, 'usuarios/login.html', {'FormularioLogin': FormularioLogin})

def autenticar(request):
    """View que verificará as informações de login digitadas pelo usuário"""
    form = FormularioLogin(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        senha = form.cleaned_data['senha']
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.senha == senha:
                request.session['id_usuario'] = usuario.id_usuario
                return redirect('calculadora')
        except Usuario.DoesNotExist:
            return redirect('login')
    return redirect('login')
    
def cadastrar(request):
    """View que retornará a página de cadastro/criação de conta na calculadora"""
    return render(request, 'usuarios/cadastrar.html', {'FormularioCadastro': FormularioCadastro})

def salvar_cadastro(request):
    """View que verificará as informações de cadastro do usuário e criará um novo usuário"""
    form = FormularioCadastro(request.POST)
    if form.is_valid():
        nome = form.cleaned_data['nome']
        email = form.cleaned_data['email']
        senha = form.cleaned_data['senha']
        usuario = Usuario.objects.create(nome=nome, email=email, senha=senha)
        return redirect('login')
    return redirect('cadastrar')