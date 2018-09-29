from django.shortcuts import render

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
    drinkResults = {'Test 1', 'Test 2'}

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