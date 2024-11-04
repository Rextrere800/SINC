from django.db import models
from django import forms

# Create your models here.
class Matches(models.Model):
    username = models.CharField(max_length=40)
    posiblesmatches = models.CharField(max_length=1000)
    matches = models.CharField(max_length=1000)
    no_matches = models.CharField(max_length=1000)
class MatchForm(forms.Form):
    match = forms.CharField(label="match", max_length=2)
