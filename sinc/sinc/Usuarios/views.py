from django.shortcuts import render, redirect
from .forms import *
# Create your views here.
def login(request):
    return render(request, 'login.html')
def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            return redirect('login.html')
    else:
        form=Register()
    return render(request, 'register.html')

def registered(request):
    if request.method == 'POST':
        form = Register(request.POST)
        print(form)
        if form.is_valid():
            # Procesar los datos del formulario
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Crear un nuevo usuario
            print(username)
            print(email)
            print(password)
            # Redirigir al usuario a una página de éxito
            return 'registrado'
    return render(request, 'register.html')
def prueba(request):
    if request.method == 'POST':

    return render(request,'prueba.html')