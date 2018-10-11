from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from . import cocktaildbapi as cdb

# Create your views here.
def index(request):
    context = {
        'activePage': 'Home',
        'currentUser': ''
    }
    return render(request, 'DrinkBeyondThePossible/home.html', context=context)

def detail(request):
    context = {}
    return render(request, 'DrinkBeyondThePossible/detail.html', context=context)

def results(request):
    drinkResults = []
    if 'ingredient' in request.GET:
        searchResults = []
        for ingredient in request.GET.getlist('ingredient'):
            matchingResult = cdb.searchMatchingDrinks(ingredient)
            searchResults.append(set(matchingResult.drinks))

        drinkResults = list(set.intersection(*searchResults))

    context = {'drinkResults': drinkResults}
    return render(request, 'DrinkBeyondThePossible/search_results.html', context=context)

def login(request):
    context = {}
    return render(request, 'DrinkBeyondThePossible/login.html', context=context)

def logout(request):
    context = {

    }
    return render(request, 'DrinkBeyondThePossible/logout.html', context=context)

def manage(request):
    context = {
        'activePage': 'Account'
    }
    return render(request, 'DrinkBeyondThePossible/account_management.html', context=context)

def newCustomDrink(request):
    context = {
        'activePage': 'Account'
    }
    return render(request, 'DrinkBeyondThePossible/new_custom_drink.html', context=context)

def ingredientList(request):
    context = {
        'activePage': 'Account'
    }
    return render(request, 'DrinkBeyondThePossible/ingredient_list.html', context=context)

def recipeList(request):
    context = {
        'activePage': 'Account'
    }
    return render(request, 'DrinkBeyondThePossible/custom_drinks.html', context=context)