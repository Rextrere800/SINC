from django.db import models

# Create your models here.
class Usuario(models.Model):
    username = models.CharField(max_length=40)
    email= models.CharField(max_length=320)
    password = models.CharField(max_length=100)

class Perfil(models.Model):
    username = models.CharField(max_length=40)
    real_name = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    career = models.CharField(max_length=40)
    interests = models.CharField(max_length=128)