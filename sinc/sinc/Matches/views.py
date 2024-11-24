import random
from django.shortcuts import render, redirect,get_object_or_404
from Matches.models import *
from Usuarios.models import Perfil
from Usuarios.views import FiltroIntereses
# Create your views here.

Usuariogustar=''

def match(request):
    perfil_id = request.session.get('usuario_id')
    if not perfil_id:
        return redirect('')

    Matches.objects.get_or_create(id=perfil_id)
    print('\033[92m[Perfilid]:\033[00m ',perfil_id)
    perfil = get_object_or_404(Matches,id=perfil_id)
    print('\033[92m[Perfilid]:\033[00m ',perfil)
    FiltroIntereses(perfil_id)
    posibles_matches = Matches.objects.raw('''SELECT id,posiblesmatches FROM Matches_matches WHERE id = {}'''.format(perfil_id))
    #print(f'\n\n\n\nID:{perfil.id}\nmatches:{perfil.matches}\nno_matches:{perfil.no_matches}\n\n\n\n')
    madeMatches = Matches.objects.raw('''SELECT id,matches FROM Matches_matches WHERE id = {}'''.format(perfil_id))
    posibles_matches = Matches.objects.raw('''SELECT id,posiblesmatches FROM Matches_matches WHERE id = {}'''.format(perfil_id))
    posibles_matches1 = (next(iter(posibles_matches)).posiblesmatches).split(";")
    del posibles_matches1[-1]
    #print(posibles_matches1)
    no_matches = Matches.objects.raw('''SELECT id,no_matches FROM Matches_matches WHERE id = {}'''.format(perfil_id))
    madeMatches = [a.matches for a in madeMatches]
    posibles_matches = [a.posiblesmatches for a in posibles_matches]
    no_matches = [a.no_matches for a in no_matches]
    for a in range(len(posibles_matches)):
        if posibles_matches[a] in no_matches[0]:
            posibles_matches.pop(a)
        elif posibles_matches[a] in madeMatches[0]:
            posibles_matches.pop(a)
    #print(posibles_matches)
    # Llamamos al id del perfil iniciado, en caso de no encontrarlo, redirigir a login
    print("ooooo")
    if request.method == 'POST':
        print("iiiiii")
        matchAnterior=request.session.get('matchActual')
        matchAnterior=get_object_or_404(Perfil, usuario_id=matchAnterior)
        print("aaaaa")
        form = MatchForm(request.POST)
        if form.is_valid():
            matching = form.cleaned_data['match']
            matching = matching == "si"
            try:
                perfil_id = request.session.get('usuario_id')
            except:
                return redirect('login')
    # Aqui usamos la funcion FiltroIntereses con tal de generar los posibles matches
            if matching:
                #print('\033[92m[INFORMACION]:\033[00m ',perfil_id,'hizo match con',matchAnterior.id)
                perfil.matches=madeMatches[0]+';'+str(matchAnterior.usuario_id)
            elif not matching:
                perfil.no_matches=no_matches[0]+';'+str(matchAnterior.usuario_id)
            stringvacio=""
            #print("\033[92m[POSIBLESMATCHES1]:\033[00m",posibles_matches1)
            #print("\033[92m[MATCHANTERIOR ID]:\033[00m",matchAnterior.id)
            if str(matchAnterior.usuario_id) in posibles_matches1:
                posibles_matches1.remove(str(matchAnterior.usuario_id))
            for x in posibles_matches1:
                stringvacio+=x+";"
            #print("\033[92m[STRINGVACIO]:\033[00m",stringvacio)
            perfil.posiblesmatches=stringvacio
            perfil.save()
        Otroperfil, created=Matches.objects.get_or_create(id=matchAnterior.usuario_id)
        matches_otroperfil = Otroperfil.matches.split(";") if Otroperfil.matches else []
        print("estoo")
        print(matches_otroperfil)
        if str(perfil_id) in matches_otroperfil:
            matchdef=str(perfil.matchdefinitivo)+";"+str(matchAnterior.usuario_id)
            perfil.matchdefinitivo=matchdef
            perfil.save()
            return redirect('match_confirmacion', match_id=matchAnterior.usuario_id)
    print("ññññññ")
    perfil_matches, created = Matches.objects.get_or_create(id=perfil_id)
    print(perfil_id)
    posibles_matches = perfil_matches.posiblesmatches.split(';') if perfil_matches.posiblesmatches else []     
    print(posibles_matches)
    try:
        matchActual = random.choice(posibles_matches)
    except IndexError:
        print("\033[91m[ERROR]:\033[00m no hay usuarios para hacer match, redirigiendo al usuario a su perfil")
        return redirect('perfil')
    while matchActual == '':
        matchActual = random.choice(posibles_matches)
    request.session['matchActual'] = matchActual
    #print(f'\n\n\n\nID:{perfil.id}\nmatches:{perfil.matches}\nno_matches:{perfil.no_matches}\n\n\n\n')
    matchActual=get_object_or_404(Perfil, usuario_id=matchActual)
    print(matchActual)
    return render(request,'matches.html',{"matchActual":matchActual})
    matchActual=get_object_or_404(Perfil, id=matchActual)
    matches = []
    tipo_contacto=[]
    nose = madeMatches[0].split(';')
    del nose[0]
    for a in nose:
        a=get_object_or_404(Perfil, id=a)
        contactos = a.Metodo_contacto.split(';')
        for contacto in range(len(contactos)):
            tipo_contacto.append(contactos[contacto].split('.')[1])
        matches.append({'username':a.username,'platform':tipo_contacto,'url':contactos})
        tipo_contacto=[]
    print(f'\n\n\n\n\n\n','matches hechos: ', (madeMatches),'\n\n\n\n')
    return render(request,'matches.html',{"matchActual":matchActual,'matches':matches})

def match_confirmacion(request, match_id):
    perfil_match = get_object_or_404(Perfil, usuario_id=match_id)
    return render(request, 'match_confirmacion.html', {"perfil_match": perfil_match})

