from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import datetime

from django.contrib.contenttypes.fields import GenericRelation
#from star_ratings import get_star_ratings_rating_model_name

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile(user=instance).save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Drink(models.Model):
    name = models.CharField(max_length=50, default='')
    cocktaildb_id = models.IntegerField()

class Tag(models.Model): 
    name = models.CharField(max_length=20, default='')
    drink_ID = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    drinkID = models.IntegerField()
    message = models.CharField(max_length=2000)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    @property
    def is_updated(self): 
        #return str(self.created_time) == str(self.updated_time)
        return self.updated_time > self.created_time + datetime.timedelta(seconds=5)

class drinkRating(models.Model):
    drink_id = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    #rating = GenericRelation(get_star_ratings_rating_model_name(), related_query_name='ratedrink')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # def str(self):
    #     return self.name

class Ingredient_List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.CharField(max_length=50)

    class Meta:
        unique_together = ('user', 'ingredient')
        ordering = ['user']

class customDrink(models.Model):
    id = models.AutoField(primary_key=True)
    drink_name = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=2000)
    instructions = models.CharField(max_length = 2000)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('drink_name', 'user')

class customRecipe(models.Model):
    custom_name = models.CharField(max_length=50)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ingredient = models.CharField(max_length=50)

class favoriteDrink(models.Model):
    drink_name = models.CharField(max_length=50)
    drink_id = models.IntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('drink_id', 'user')
