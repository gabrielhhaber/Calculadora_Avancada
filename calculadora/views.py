from django.shortcuts import render

def index(request):
    """View que retornará a página inicial da calculadora"""
    return render(request, 'calculadora/index.html')

def calculadora(request):
    """View que retornará a página da calculadora propriamente dita, permitindo realizar operações e ver o histórico"""
    return render(request, "calculadora/calculadora.html")