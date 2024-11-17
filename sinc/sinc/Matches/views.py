import random
from django.shortcuts import render, redirect,get_object_or_404
from Matches.models import *
from Usuarios.models import Perfil
from Usuarios.views import FiltroIntereses
# Create your views here.

Usuariogustar=''

def match(request):
    """idprincipal="1"
    idgustar = "2"
    if Usuariogustar == True:
        a = Matches.objects.get(id=idprincipal)
        b = a.matches
        if idgustar in b:
            match=True
        else:
            a = Matches.objects.get(id=idgustar)
            b = idprincipal + ";"
            a.matches += b
            a.save()
            match=False
    else:
        match=False
    return(match)"""
    perfil_id = request.session.get('perfil_id')
    Matches.objects.get_or_create(id=perfil_id)
    perfil = get_object_or_404(Matches,id=perfil_id)
    FiltroIntereses(perfil_id)
    print(f'\n\n\n\nID:{perfil.id}\nmatches:{perfil.matches}\nno_matches:{perfil.no_matches}\n\n\n\n')
    madeMatches = Matches.objects.raw('''SELECT id,matches FROM Matches_matches WHERE id = {}'''.format(perfil_id))
    posibles_matches = Matches.objects.raw('''SELECT id,posiblesmatches FROM Matches_matches WHERE id = {}'''.format(perfil_id))
    no_matches = Matches.objects.raw('''SELECT id,no_matches FROM Matches_matches WHERE id = {}'''.format(perfil_id))
    madeMatches = [a.matches for a in madeMatches]
    posibles_matches = [a.posiblesmatches for a in posibles_matches]
    no_matches = [a.no_matches for a in no_matches]
    for a in range(len(posibles_matches)):
        if posibles_matches[a] in no_matches:
            posibles_matches.pop(a)
        elif posibles_matches[a] in madeMatches:
            posibles_matches.pop(a)
    # Llamamos al id del perfil iniciado, en caso de no encontrarlo, redirigir a login
    if request.method == 'POST':
        matchAnterior=request.session.get('matchActual')
        matchAnterior=get_object_or_404(Perfil, id=matchAnterior)
        form = MatchForm(request.POST)
        if form.is_valid():
            matching = form.cleaned_data['match']
            matching = matching == "si"
            try:
                perfil_id = request.session.get('perfil_id')
            except:
                return redirect('login')
    # Aqui usamos la funcion FiltroIntereses con tal de generar los posibles matches
            if matching:
                print('match hecho!!!!')
                perfil.matches=madeMatches[0]+';'+str(matchAnterior.id)
                perfil.save()
            elif not matching:
                perfil.no_matches=no_matches[0]+';'+str(matchAnterior.id)
                perfil.save()
    try:
        matchActual = random.choice(posibles_matches[0].split(';'))
    except IndexError:
        print("ERROR: no hay usuarios para hacer match, redirigiendo al usuario a su perfil")
        return redirect('perfil')
    while matchActual == '':
        matchActual = random.choice(posibles_matches[0].split(';'))
    request.session['matchActual'] = matchActual
    print(f'\n\n\n\nID:{perfil.id}\nmatches:{perfil.matches}\nno_matches:{perfil.no_matches}\n\n\n\n')
    matchActual=get_object_or_404(Perfil, id=matchActual)
    return render(request,'matches.html',{"matchActual":matchActual})