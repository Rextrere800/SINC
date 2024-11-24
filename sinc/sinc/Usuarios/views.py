from django.shortcuts import render, redirect, get_object_or_404
from .models import * 
from .forms import PerfilForm
from Matches.models import Matches
import os

def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        login_check=False
        usuario_id = None
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            real_password=Usuario.objects.raw('''SELECT  id,password FROM Usuarios_usuario WHERE username = "{}"'''.format(username))
            for a in real_password:
                if a.password == password:
                    login_check=True
                    usuario_id = a.id
        if login_check:
            request.session['usuario_id'] = usuario_id
            return redirect("match")
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
                    
                    usuario = Usuario.objects.create(username=username, email=email, password=password)
                    request.session['usuario_id'] = usuario.id
                    #print(f"\033[92m[INFORMACION]:\033[00m Usuario creado con los siguientes datos: \nnombre de usuario: {username}\ncontraseña: {password}\ncorreo: {email}")
                    instance = form.save(commit=False)
                    #print(Usuario.objects.values_list("username",flat=True))
                    #print(username in Usuario.objects.values_list('username',flat=True))
                    return redirect("crear_perfil")
    return redirect('/register')

def crear_perfil(request):
    #usuario = Usuario.objects.get(id=usuario_id)
    #print(usuario)
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            try:
                print("\033[92m[INFORMACION]:\033[00m La id es",perfil.id)
            except:
                print("\033[91m[ERROR]:\033[00m fallo al crear perfil")
            usuario_id = request.session.get('usuario_id')
            print("\033[92m[INFORMACIOON]:\033[00m La id es",usuario_id)
            if not usuario_id:
                # Si no hay un usuario en la sesión, redirige al inicio de sesión o muestra un error
                return redirect('login')

            # Asigna el usuario al perfil
            perfil.usuario = Usuario.objects.get(id=usuario_id)
            perfil.save()  # Guarda el perfil con el usuario asignado

            request.session['perfil_id'] = perfil.id
            return redirect('perfil_creado') 
    else:
        form = PerfilForm()
    
    return render(request, 'crear_perfil.html', {'form': form})

def perfil(request):
    perfil_id = request.session.get('perfil_id')
    perfil=get_object_or_404(Perfil, id=perfil_id)
    return render(request, 'perfiles.html',{'perfil':perfil})

def perfil_creado(request):
    return render(request, 'perfil_creado.html')

def FiltroIntereses(principalid):
    perfil_matches, created = Matches.objects.get_or_create(id=principalid)
    matches = perfil_matches.matches.split(';') if perfil_matches.matches else []
    no_matches = perfil_matches.no_matches.split(';') if perfil_matches.no_matches else []
    p = Perfil.objects.values('usuario_id')
    idlista = [int(p['usuario_id']) for p in Perfil.objects.values('usuario_id')]
    #print("\033[92m[INFORMACION]:\033[00m",idlista)
    
  
    try:
        indice = idlista.index(int(principalid))
    except ValueError:
        print(f"\033[91m[ERROR]:\033[00m El ID principal {principalid} no está en la lista.")
        return
    
   
    p = Perfil.objects.values('interests')
    Plista = [p['interests'] for p in Perfil.objects.values('interests')]
    
    interesprincipal = Plista.pop(indice) + ";"
    idprincipal = idlista.pop(indice)
    
    listausar=[]
    c=0

    for n in Plista:
        x=idlista[c]
        listausar.append([n,x])
        c+=1
    print("\033[92m[INFORMACION]:\033[00m",listausar)


    listaprincipal = []
    
    x = ''
    for n in interesprincipal:
        if n != ";":
            x += n
        else:
            print("\033[92m[INFORMACION]:\033[00m",x)
            listaprincipal.append(x)
            x = ""
    #print("\033[92m[INFORMACION]:\033[00m",listaprincipal)

    indicescoincidencias = []
    
    for n in listaprincipal:
        for z in listausar:
            if n in z[0] and z[1] not in indicescoincidencias:
                indicescoincidencias.append(z[1])

    #print("\033[92m[INFORMACIOOON]:\033[00m",matches)
    #print("\033[92m[INFORMACIOOON]:\033[00m",no_matches)
    coincidenciasid = ""
    print("\033[92m[INDICECOINCIDENCIAS]:\033[00m",indicescoincidencias)
    for n in indicescoincidencias:
        if str(n) not in matches and str(n) not in no_matches:
            coincidenciasid += str(n) + ";"
    print("\033[92m[COINCIDENCIASID]:\033[00m",coincidenciasid)

    Matches.objects.update_or_create(id=idprincipal, defaults={'posiblesmatches': coincidenciasid})


# get perfil