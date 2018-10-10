from django.db import models

# Create your models here.

# Note: These models were made to facilitate the uploading of custom drinks to database. 
# There are probably some mistakes

class Users(models.Model):
	username = models.CharField(max_length=15)
	salted_password = models.CharField(max_length=15)
	salt = models.CharField(max_length=15)

class Drink(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
        return self.name 

class Comments(models.Model):
	user_id = models.ForeignKey(Users, unique=True)
	drink_name = models.ForeignKey(Drink, unique=True)
	message = models.CharField(max_length=2000)

class drinkRating(models.Model):
	drink_name = models.ForeignKey(Drink, unique=True)
	rating = models.IntegerField()


class Ingredient(models.Model):
	ingredient = models.CharField(max_length=50)
	user_id = models.ForeignKey(Users)

class Ingredient_List(models.Model):
	ingredients = models.ForeignKey(Ingredient, unique=False)
	user_id = models.ForeignKey(Users)

class customDrink(models.Model):
	name = models.ForeignKey(Drink, unique=True)
	ingredients = models.ForeignKey(Ingredient_List, unique=False)
	description = models.CharField(max_length=2000)
	image = models.ImageField(upload_to='uploads/', blank=True, null=True)
	user_id = models.ForeignKey(Users, unique=True)

class customRecipe(models.Model):
	custom_name = models.CharField(max_length=50, primary_key=True)
	user_id = models.ForeignKey(Users, unique=True)
	ingredients = models.ForeignKey(Ingredient_List)

