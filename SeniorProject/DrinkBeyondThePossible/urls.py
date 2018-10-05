from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account', views.manage, name='manage'),
    path('account/ingredients', views.ingredientList, name='ingredientList'),
    path('account/recipes', views.recipeList, name='recipes'),
    path('account/recipes/add', views.newCustomDrink, name='recipeEntry'),
    path('detail', views.detail, name='detail'),
    path('results', views.results, name='results'),
    path('account/manage', views.editAccount, name='editAccount'),
    #path('account/manage/submit', views.redirectH
    path('create_account', views.createAccount, name='createAccount')
]
