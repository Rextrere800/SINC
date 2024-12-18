from django import forms
from Usuarios.models import Perfil

class Register(forms.Form):
    username = forms.CharField(label = "Nombre de usuario", max_length=40)
    email= forms.CharField(label="Correo electrónico", max_length=120)
    password=forms.CharField(label="Contraseña",max_length=100)

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['real_name', 'description', 'career', 'interests', "Metodo_contacto"]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'interests': forms.TextInput(attrs={'placeholder': 'Intereses separados por punto y coma'}),
            "Metodo_contacto": forms.TextInput(attrs={"placeholder": "Ingresa tu numero o tu instagram"})
        }
