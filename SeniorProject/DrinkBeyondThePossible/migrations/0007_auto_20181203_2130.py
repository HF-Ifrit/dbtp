# Generated by Django 2.1.1 on 2018-12-04 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DrinkBeyondThePossible', '0006_customdrink_instructions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customrecipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DrinkBeyondThePossible.Profile'),
        ),
    ]