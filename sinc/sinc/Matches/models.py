from django.db import models

# Create your models here.
class Matches(models.Model):
    username = models.CharField(max_length=40)
    matches = models.CharField(max_length=1000)