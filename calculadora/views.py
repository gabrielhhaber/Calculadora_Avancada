from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Operacao
from usuarios.models import Usuario
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    """View que retornará a página inicial da calculadora"""
    return render(request, 'calculadora/index.html')

def calculadora(request):
    """View que retornará a página da calculadora propriamente dita, permitindo realizar operações e ver o histórico"""
    id_usuario = request.session['id_usuario']
    return render(request, 'calculadora/calculadora.html', {'id_usuario': id_usuario})

def listar_operacoes_usuario(request, id_usuario):
    """View que recebe o id de um usuário e retorna uma lista contendo suas operações em JSON"""
    try:
        usuario = Usuario.objects.get(id_usuario=id_usuario)
        operacoes = Operacao.objects.filter(id_usuario=usuario)
        operacoes_list = [model_to_dict(operacao) for operacao in operacoes]
        return JsonResponse({'operacoes': operacoes_list})
    except Exception as e:
        return HttpResponseBadRequest('não foi possível listar as operações para este usuário.')

@csrf_exempt
def registrar_operacao(request):
    """View que recebe uma operação em JSON e cria uma operação no banco de dados para um determinado usuário."""
    try:
        data = json.loads(request.body)
        usuario = Usuario.objects.get(id_usuario=data['id_usuario'])
        operacao = Operacao.objects.create(id_usuario=usuario, parametros=data['parametros'], resultado=data['resultado'])
        return JsonResponse({'operacao': model_to_dict(operacao)})
    except Exception as e:
        return HttpResponseBadRequest('Não foi possível registrar a operação para este usuário.')