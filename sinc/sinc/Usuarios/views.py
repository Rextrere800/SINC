from django.shortcuts import render, redirect
from .models import *
#from django.https import HttpRepo
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
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print("El usuario es",username)
            print("El correo es", email)
            print("La clave es", password)
            mayus = 0 
            num = 0
            symbol = 0
            passCheck = False
            passMail = True
            passUser = False
            if len(username) >=5:
                passUser=True
            if len(email.split('@')) == 2:
                for a in email.split('@')[1].split('.'):
                    if a == '':
                        passMail=False
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
                    print("ta bien")
                    passCheck = True
            if passCheck and passMail and passUser:
                Usuario.objects.create(username=username,email=email,password=password)
                print(Usuario.objects.values_list("username",flat=True))
                return redirect("/")
            return redirect('/register')
    return render(request, 'register.html')
def prueba(request):
    if request.method == 'POST':
        form = Register(request.POST)
        print(form)
    return render(request,'prueba.html')