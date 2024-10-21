from django.shortcuts import render
from Matches.models import Matches
from Usuarios.models import Perfil
# Create your views here.

Usuariogustar=''

def match():
    idprincipal="1"
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
    return(match)
        



        
        
        


    


        
    
        