from django.shortcuts import render
#from .forms import EditAccountForm
from .forms import EditAccountnameForm
from .forms import EditEmailForm
from .forms import EditPasswordForm

from .forms import NewAccountForm
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from . import cocktaildbapi as cdb
from .models import *
from .forms import NewDrinkForm, NewCommentForm

# Create your views here.
def index(request):
    context = {
        'activePage': 'Home',
        'currentUser': ''
    }
    return render(request, 'DrinkBeyondThePossible/home.html', context=context)

def detail(request, drinkID):
    drinkResult = cdb.SearchResult(cdb.idApiCall(drinkID))
    #comments = Comment.objects.filter(drinkID=drinkID)
    comments = Comment.objects.all()
    
    if request.method == 'POST':
        cform = NewCommentForm(request.POST)

        if cform.is_valid():
            #cform = cform.save(commit=False)
            #cform.user = request.user.username
            #cform.user = request.user.profile
            ##cform.drinkID = drinkID
            #drink_id = Drink.objects.filter(cocktaildb_id=drinkID)[0]
            #cform.drinkID = drink_id
            cform.drinkID = drinkID
            cform.save()
            return HttpResponseRedirect('/')
        
    else:
        cform = NewCommentForm()
    context = {'drink': drinkResult.drinks[0], 'comments': comments, 'commentform': cform}
    return render(request, 'DrinkBeyondThePossible/detail.html', context=context)

def results(request):
    drinkResults = []
    ingredients = []
    if 'ingredient' in request.GET: # Get ingredient search parameters from request
        searchResults = []
        ingredients = request.GET.getlist('ingredient')
        for ingredient in ingredients:
            matchingResult = cdb.searchMatchingDrinks(ingredient)
            searchResults.append(set(matchingResult.drinks))

        drinkResults = list(set.intersection(*searchResults))

    context = {'drinkResults': drinkResults, 'searchIngredients': ingredients}
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

# def newCustomDrink(request):
#     context = {
#         'activePage': 'Account'
#     }
#     return render(request, 'DrinkBeyondThePossible/new_custom_drink.html', context=context)

def ingredientList(request):
   
    context = {
       'activePage': 'Account'
    }


    if request.method == 'POST':
        pass
    else:
        return render(request, 'DrinkBeyondThePossible/ingredient_list.html', context=context)


def recipeList(request):
    context = {
        'activePage': 'Account'
    }
    return render(request, 'DrinkBeyondThePossible/custom_drinks.html', context=context)


def editAccount(request):
    
    #form = EditAccountForm()
    usernameForm = EditAccountnameForm()
    emailForm = EditEmailForm()
    passwordForm = EditPasswordForm()

    return render(request, 'DrinkBeyondThePossible/edit_account.html', {'usernameForm': usernameForm, 'emailForm': emailForm, 'passwordForm': passwordForm})


def editUsername(request):

    if request.method == 'POST':
        form = EditAccountnameForm(request.POST)

        if form.is_valid():
            user = request.user
            user.username=form.cleaned_data['account_name']
            user.save()

    return HttpResponseRedirect('/')


def editEmail(request):

    if request.method == 'POST':
        form = EditEmailForm(request.POST)

        if form.is_valid():
            user = request.user
            user.email=form.cleaned_data['email']
            user.save()

    return HttpResponseRedirect('/')


def editPassword(request):

    if request.method == 'POST':
        form = EditEmailForm(request.POST)

        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['password'])
            user.save()


    return HttpResponseRedirect('/')


def createAccount(request):

    if request.method == 'POST':
        form = NewAccountForm(request.POST)

        if form.is_valid():

        # create account
            User.objects.create_user(
                username=form.cleaned_data['account_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            return HttpResponseRedirect('/')
    else:
        form = NewAccountForm()

    return render(request, 'DrinkBeyondThePossible/create_account.html', {'form': form})


def newCustomDrink(request):
    if request.method == 'POST':
        form = NewDrinkForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        
    else:
        form = NewDrinkForm()

    return render(request, 'DrinkBeyondThePossible/new_custom_drink.html', {'form': form})



def viewFavoriteDrinks(request):
    

    if request.method == 'GET':
        
        fav_drinks = favoriteDrink.objects.filter(user=request.user.profile)
        
        #print(fav_drinks)

        if not fav_drinks:
            context = {'fav_drinks': None}
        else:
            context = {'fav_drinks': fav_drinks}
    
        return render(request, 'DrinkBeyondThePossible/display_favorite_drinks.html', context);

    else:
        return None
