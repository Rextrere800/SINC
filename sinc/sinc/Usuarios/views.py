from django.shortcuts import render, redirect
from .models import *
#from django.https import HttpRepo
# Create your views here.
def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        login_check=False
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            real_password=Usuario.objects.raw('''SELECT  id,password FROM Usuarios_usuario WHERE username = "{}"'''.format(username))
            for a in real_password:
                if a.password == password:
                    login_check=True
        if login_check:
            print('Iniciado sesion')
    return render(request, 'login.html')
def register(request):
    return render(request, 'register.html')

def registered(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            mayus = 0 
            num = 0
            symbol = 0
            passCheck = False
            passMail = False
            passUser = False
            if not (username in Usuario.objects.values_list('username',flat=True) or email in Usuario.objects.values_list('email',flat=True)):
                if len(username) >=5:
                    passUser=True
                if len(email.split('@')) == 2 and email.split('@')[1]=='usm.cl':
                    passMail=True
                else:
                    passMail=False
                if len(password) >=7:
                    for char in password:
                        if char.isupper():
                            mayus+=1
                        elif char.isnumeric():
                            num+=1
                        elif not (char.islower()):
                            symbol+=1
                    if mayus>=1 and num>=1 and symbol>=1:

                        passCheck = True
                if passCheck and passMail and passUser:
                    Usuario.objects.create(username=username,email=email,password=password)
                    print(f"Usuario creado con los siguientes datos: \nnombre de usuario: {username}\ncontraseña: {password}\ncorreo: {email}")
                    #print(Usuario.objects.values_list("username",flat=True))
                    #print(username in Usuario.objects.values_list('username',flat=True))
                    return redirect("/")
    return redirect('/register')