# Generated by Django 2.1.1 on 2018-10-26 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DrinkBeyondThePossible', '0007_auto_20181026_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DrinkBeyondThePossible.Profile'),
        ),
    ]