from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# Note: These models were made to facilitate the uploading of custom drinks to database. 
# There are probably some mistakes

# TODO: remove, bad duplicate of auth.models
class Users(models.Model):
    username = models.CharField(max_length=15)
    salted_password = models.CharField(max_length=15)
    salt = models.CharField(max_length=15)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Drink(models.Model):
    name = models.CharField(max_length=50)
    cocktaildb_id = models.IntegerField()

class Comment(models.Model):
    user_id = models.OneToOneField(Profile, on_delete=models.CASCADE)
    drink_name = models.OneToOneField(Drink, on_delete=models.CASCADE)
    message = models.CharField(max_length=2000)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

class drinkRating(models.Model):
    drink_name = models.OneToOneField(Drink, on_delete=models.CASCADE)
    rating = models.IntegerField()


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=50)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Ingredient_List(models.Model):
    ingredients = models.ForeignKey(Ingredient, unique=False, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

class customDrink(models.Model):
    name = models.OneToOneField(Drink, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient_List, unique=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    user_id = models.OneToOneField(Profile, on_delete=models.CASCADE)

class customRecipe(models.Model):
    custom_name = models.CharField(max_length=50, primary_key=True)
    user_id = models.OneToOneField(Profile, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient_List, on_delete=models.CASCADE)

class favoriteDrink(models.Model):
    drink_name = models.ForeignKey(Drink, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
