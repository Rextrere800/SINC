from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Perfil
from .views import FiltroIntereses

@receiver(post_save, sender=Perfil)
def actualizar_matches(sender, instance, **kwargs):
    FiltroIntereses()
