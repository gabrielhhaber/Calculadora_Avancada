from django import forms
from .models import Usuario

class FormularioLogin(forms.Form):
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)

class FormularioCadastro(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha']
        help_texts = {
            'nome': 'Máximo de 16 caracteres',
            'email': 'Exemplo: teste@email.com',
            'senha': 'Máximo de 32 caracteres'
        }