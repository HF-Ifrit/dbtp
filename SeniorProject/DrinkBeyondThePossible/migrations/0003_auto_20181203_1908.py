# Generated by Django 2.1.1 on 2018-12-03 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DrinkBeyondThePossible', '0002_auto_20181203_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drinkrating',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]
