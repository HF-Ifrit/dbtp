import asyncio
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
#from .forms import EditAccountForm
import re
from . import cocktaildbapi as cdb
from .models import *
from .forms import NewTagsForm, NewDrinkForm, NewCommentForm, NewAccountForm, EditPasswordForm, EditEmailForm, EditAccountnameForm, EditCommentForm

# Create your views here.
def index(request):

    ingredients = request.COOKIES.get('ingredients', -1);


    context = {
        'activePage': 'Home',
        'currentUser': '',
        'ingredients': ingredients
    }
    return render(request, 'DrinkBeyondThePossible/home.html', context=context)

def tagList(request, tagname):
    # Get querylist of all drinks that hold the tag name
    tags_for_drinks = Tag.objects.filter(name=tagname)
    # Extract drink_id's for each tag for query
    drinks = [drink.drink_ID for drink in tags_for_drinks]
    drink_list = []

    for drink_id in drinks:
        drinkResult = cdb.get_drink_details(drink_id)
        drink_list.append(drinkResult)



    context = {
        'drinks': drink_list
    }

    return render(request, 'DrinkBeyondThePossible/tag.html', context=context)




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
            comment = Comment.objects.create(message=cform.cleaned_data['message'], 
                user=request.user.profile, drinkID=drinkID)
            comment.save()

        editcform = EditCommentForm(request.POST)
        if editcform.is_valid():
            new_message = editcform.cleaned_data['message']
            c_id = editcform.cleaned_data['c_id']
            comment_to_be_changed = Comment.objects.get(id=c_id)
            comment_to_be_changed.message = new_message
            comment_to_be_changed.save()

        tagform = NewTagsForm(request.POST)

        if tagform.is_valid():
            tag_string = tagform.cleaned_data['tags']
            tag_list = [x.strip() for x in tag_string.split(',')] # contains parsed tags from user
            tags_of_drink = [i.name for i in Tag.objects.filter(drink_ID=drinkID)] # contains existing tags for drink
            for tag in tag_list:
                # ignore any invalid tags
                if re.match("^[a-zA-Z]*$", tag) and tag not in tags_of_drink:
                    t = Tag.objects.create(name=tag, drink_ID=drinkID)
                    t.save()

    comments = Comment.objects.filter(drinkID=drinkID)
    cform = NewCommentForm()
    editcform = EditCommentForm()
    tagform = NewTagsForm()
    
    tags = [i.name for i in Tag.objects.filter(drink_ID=drinkID)]

    context = {
        'drink': drinkResult, 
        'user_ingredients': user_ingredients, 
        'comments': comments, 
        'commentform': cform, 
        'recommended_drinks': recommended_drinks, 
        'tagform': tagform,
        'tags': tags,
        'editcform': editcform
    }
    return render(request, 'DrinkBeyondThePossible/detail.html', context=context)

def results(request):
    drinkResults = []
    ingredients = []
    if 'ingredient' in request.GET: # Get ingredient search parameters from request
        searchResults = []
        ingredients = request.GET.getlist('ingredient')
        #drinkResults = cdb.find_matching_drinks(ingredients)
        for ingredient in ingredients:
            matchingResult = cdb.searchMatchingDrinks(ingredient)
            if type(matchingResult) is cdb.SearchResult:
                searchResults.append(set(matchingResult.drinks))
        
        if searchResults:
            drinkResults = list(set.intersection(*searchResults))

    #response = render_to_response(request, 'DrinkBeyondThePossible/search_results.html', context={'drinkResults': drinkResults, 'searchIngredients': ingredients})

    #if not request.user.is_authenticated:
        #pass
        #response = request.set_cookie('ingredients', ingredients)
        #response = render_to_response(request, 'DrinkBeyondThePossible/search_results.html', context={'drinkResults': drinkResults})

    #    request.set_cookie('ingredients', ingredients)

    print(ingredients)
    context = {'drinkResults': drinkResults, 'searchIngredients': ingredients}
    return render(request, 'DrinkBeyondThePossible/search_results.html', context=context)

    #print(ingredients)
    #return response

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

            if request.COOKIES.get('ingredients', -1) != -1:
                ingredients = request.COOKIES.get('ingredients', -1)
                for ingredient in ingredients:
                    ingredientObject = Ingredient_List.objects.create(user=request.user, ingredient=ingredient)
                    ingredientObject.save()

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
