from django.db import models
from usuarios.models import Usuario

class Operacao(models.Model):
    id_operacao = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='operacoes')
    parametros = models.CharField(max_length=100)
    resultado = models.CharField(max_length=100)
    dt_inclusao = models.DateField(auto_now_add=True)