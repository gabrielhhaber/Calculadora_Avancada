from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Operacao
from usuarios.models import Usuario
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
        operacoes = usuario.operacoes.all().order_by('-id_operacao')
        operacoes_list = list(operacoes.values(
            'id_operacao', 'id_usuario', 'parametros', 'resultado', 'dt_inclusao'))
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
        return JsonResponse({
            'operacao': {
                'id_operacao': operacao.id_operacao,
                'id_usuario': operacao.id_usuario.id_usuario,
                'parametros': operacao.parametros,
                'resultado': operacao.resultado,
                'dt_inclusao': operacao.dt_inclusao,
            }
        })
    except Exception as e:
        return HttpResponseBadRequest("Não foi possível registrar a operação para este usuário.")

@csrf_exempt
def deletar_operacoes_usuario(request, id_usuario):
    """View que recebe o id de um usuário e deleta todas as suas operações"""
    try:
        if request.method == 'DELETE':
            usuario = Usuario.objects.get(id_usuario=id_usuario)
            usuario.operacoes.all().delete()
            return JsonResponse({'mensagem': 'Operações deletadas com sucesso'})
    except Exception as e:
        return HttpResponseBadRequest("Não foi possível deletar as operações para este usuário")
    return HttpResponseBadRequest("Não foi possível deletar as operações para este usuário")