# Generated by Django 2.1.1 on 2018-12-07 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DrinkBeyondThePossible', '0012_auto_20181207_0049'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customrecipe',
            unique_together={('custom_name', 'user', 'ingredient')},
        ),
    ]