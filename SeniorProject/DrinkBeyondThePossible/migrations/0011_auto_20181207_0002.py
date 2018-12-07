# Generated by Django 2.1.1 on 2018-12-07 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DrinkBeyondThePossible', '0010_auto_20181207_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='favoriteDrink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drink_name', models.CharField(max_length=50)),
                ('drink_id', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='DrinkBeyondThePossible.Profile')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='favoritedrink',
            unique_together={('drink_id', 'user')},
        ),
    ]
