# Generated by Django 2.1.1 on 2018-12-07 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DrinkBeyondThePossible', '0009_auto_20181206_2220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoritedrink',
            name='drink',
        ),
        migrations.RemoveField(
            model_name='favoritedrink',
            name='user',
        ),
        migrations.DeleteModel(
            name='favoriteDrink',
        ),
    ]