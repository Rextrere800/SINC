from django import forms
class Register(forms.Form):
    username = forms.CharField(label = "Nombre de usuario", max_length=40)
    email= forms.CharField(label="Correo electrónico", max_length=120)
    password=forms.CharField(label="Contraseña",max_length=100)