from django.db import models

class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=16, unique=True)
    senha = models.CharField(max_length=32)
    dt_inclusao = models.DateField(auto_now_add=True)