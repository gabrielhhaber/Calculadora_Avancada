from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name='login'),
    path('autenticar/', views.autenticar, name='autenticar'),
    path("cadastrar/", views.cadastrar, name='cadastrar'),
    path('salvar_cadastro/', views.salvar_cadastro, name='salvar_cadastro'),
]