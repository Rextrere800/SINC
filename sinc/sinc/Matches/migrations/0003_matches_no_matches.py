# Generated by Django 5.1 on 2024-11-04 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Matches', '0002_matches_posiblesmatches'),
    ]

    operations = [
        migrations.AddField(
            model_name='matches',
            name='no_matches',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]