from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calculadora/', views.calculadora, name='calculadora'),
    path('calculadora/listar_operacoes_usuario/<int:id_usuario>/', views.listar_operacoes_usuario, name='listar_operacoes_usuario'),
    path('calculadora/registrar_operacao/', views.registrar_operacao, name='registrar_operacao'),
]