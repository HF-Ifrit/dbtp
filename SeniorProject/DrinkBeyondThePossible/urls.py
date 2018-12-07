from django.urls import path, include
from django.conf.urls import url

from . import views

#app_name="ratings"

urlpatterns = [
    path('', views.index, name='index'),
    path('account', views.manage, name='manage'),
    path('account/ingredients', views.ingredientList, name='ingredientList'),
    path('account/test_ingredients_view', views.viewFavoriteDrinks, name='testIngredientView'),
    path('account/recipes', views.recipeList, name='recipes'),
    path('account/recipes/add', views.newCustomDrink, name='recipeEntry'),
    path('account/recipes/<str:recipe_name>', views.displayCustomDrinks, name='recipe'),
    path('detail/<int:drinkID>', views.detail, name='detail'),
    path('results', views.results, name='results'),
    path('account/manage', views.editAccount, name='editAccount'),
    path('create_account', views.createAccount, name='createAccount'),
    path('account/manage/edit_username', views.editUsername, name='editUsername'),
    path('account/manage/edit_email', views.editEmail, name='editEmail'),
    path('account/manage/edit_password', views.editPassword, name='editPassword'),
    path('account/favorite_drinks', views.viewFavoriteDrinks, name='favoriteDrinkList'),
    path('tag/<slug:tagname>', views.tagList, name='tag')

]
