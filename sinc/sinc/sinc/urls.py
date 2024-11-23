"""
URL configuration for sinc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Usuarios import views as usr_views
from django.conf.urls.static import static
from django.conf import settings
from Matches import views as matchs_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', usr_views.login),
    path('register/',usr_views.register),
    path('registered/',usr_views.registered,name='registered'),
    path('crear_perfil/', usr_views.crear_perfil, name='crear_perfil'),
    path('perfil_creado/', usr_views.perfil_creado, name='perfil_creado'),
    path('perfil/',usr_views.perfil,name='perfil'),
    path('match/',matchs_views.match,name='match'),
    path('match_confirmacion/<int:match_id>/', matchs_views.match_confirmacion, name='match_confirmacion'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


