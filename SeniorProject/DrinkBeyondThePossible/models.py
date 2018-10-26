from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

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
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    drinkID = models.OneToOneField(Drink, on_delete=models.CASCADE)
    message = models.CharField(max_length=2000)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

class drinkRating(models.Model):
    drink_id = models.OneToOneField(Drink, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

class Ingredient_List(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ingredient = models.CharField(max_length=50)

    class Meta:
        unique_together = ('user', 'ingredient')
        ordering = ['user']

class customDrink(models.Model):
    drink = models.OneToOneField(Drink, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient_List, unique=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

class customRecipe(models.Model):
    custom_name = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient_List, on_delete=models.CASCADE)

class favoriteDrink(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
