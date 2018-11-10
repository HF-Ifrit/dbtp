import asyncio
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
#from .forms import EditAccountForm

from . import cocktaildbapi as cdb
from .models import *
from .forms import NewTagsForm, NewDrinkForm, NewCommentForm, NewAccountForm, EditPasswordForm, EditEmailForm, EditAccountnameForm

# Create your views here.
def index(request):
    context = {
        'activePage': 'Home',
        'currentUser': ''
    }
    return render(request, 'DrinkBeyondThePossible/home.html', context=context)

def detail(request, drinkID):
    drinkResult = cdb.get_drink_details(drinkID)

    #Get recommended drink info
    recommended_drinks = cdb.find_recommended_drinks(drinkResult.ingredients)
    # for ingredient in drinkResult.drinks[0].ingredients:
    #     recommendation_result = cdb.searchMatchingDrinks(ingredient)
    #     if type(recommendation_result) is cdb.SearchResult:
    #         for drink in recommendation_result.drinks:
    #             recommended_drinks.add(drink)

    user_ingredients = []
    uid = request.user.id

    # Get the ingredient list of the user account of this session
    if request.user.is_authenticated:
        user_ingredients = [entry.ingredient for entry in Ingredient_List.objects.filter(user=uid)]

    if request.method == 'POST':
        if 'newIngredients[]' in request.POST:
            curr_user = User.objects.get(username=request.user.username)
            newIngredients = request.POST.getlist('newIngredients[]')
            for ingredient in newIngredients:
                newEntry = Ingredient_List.objects.create(user=curr_user, ingredient=ingredient)
                newEntry.save()

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

        tagform = NewTagsForm(request.POST)
        if tagform.is_valid():
            obj = tagform.save(commit=False)
            obj.user = request.user
            obj.save()
            tagform.save_m2m()



    # if request.method == 'POST':
    #     form = NewCommentForm(request.POST)

    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect('/')

    # else:
    #     form = NewCommentForm()

    #comments = Comment.objects.filter(drinkID=drinkID)
    comments = Comment.objects.all()
    cform = NewCommentForm()
    tagform = NewTagsForm()

    context = {
        'drink': drinkResult, 
        'user_ingredients': user_ingredients, 
        'comments': comments, 
        'commentform': cform, 
        'recommended_drinks': recommended_drinks, 
        'tagform': tagform
    }
    return render(request, 'DrinkBeyondThePossible/detail.html', context=context)

def results(request):
    drinkResults = []
    ingredients = []
    if 'ingredient' in request.GET: # Get ingredient search parameters from request
        searchResults = []
        ingredients = request.GET.getlist('ingredient')
        for ingredient in ingredients:
            matchingResult = cdb.searchMatchingDrinks(ingredient)
            if type(matchingResult) is cdb.SearchResult:
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

def ingredientList(request):

    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        ingredients = Ingredient_List.objects.filter(user=request.user)

        context = {
            'activePage': 'Account',
            'ingredients': ingredients
        }

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

        getOp = "Favorite Drinks"
        collection = favoriteDrink.objects.filter(user=request.user.profile)

        #fav_drinks = favoriteDrink.objects.filter(user=request.user.profile)

        #print(fav_drinks)

        if not collection:
            context = {'collection': None, 'getOp': getOp}
        else:
            context = {'collection': collection, 'getOp': getOp}

        return render(request, 'DrinkBeyondThePossible/display_favorite_drinks.html', context)

    else:
        return None
