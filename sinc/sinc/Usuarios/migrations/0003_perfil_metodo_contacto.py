# Generated by Django 5.1.3 on 2024-11-23 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0002_alter_perfil_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='Metodo_contacto',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
