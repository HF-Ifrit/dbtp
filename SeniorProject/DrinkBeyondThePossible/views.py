import re
import itertools
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.views import login_required
from django.views.decorators.http import require_http_methods
from collections import defaultdict
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
    ratings = []

    for drink_id in drinks:
        all_ratings = drinkRating.objects.filter(drink_id=drink_id)
        num_ratings = all_ratings.count()
        if num_ratings > 0:
            avg_rating = 0
            for rating in all_ratings:
                avg_rating += rating.rating
            avg_rating = round(avg_rating / num_ratings, 2)
        else:
            avg_rating = -1
        drinkResult = cdb.get_drink_details(drink_id)
        drink_list.append(drinkResult)
        ratings.append(avg_rating)

    
    z_ratings = zip(drink_list, ratings)
    z_ratings = sorted(z_ratings, key=lambda x: x[1], reverse=True)



    context = {
        'tagname': tagname.capitalize(),
        'drinks': drink_list,
        'drink_ratings': z_ratings
    }

    return render(request, 'DrinkBeyondThePossible/tag.html', context=context)

def detail(request, drinkID):
    drinkResult = cdb.get_drink_details(drinkID)
    ingredient_dict = dict(zip(drinkResult.ingredients, drinkResult.measurements))
    ingredient_dict = defaultdict(lambda: '', ingredient_dict)

    #Get recommended drink info
    recommended_drinks = cdb.find_recommended_drinks(drinkResult.ingredients)

    user_ingredients = []
    uid = request.user.id

    # Get the ingredient list of the user account of this session
    if request.user.is_authenticated:
        user_ingredients = [entry.ingredient for entry in Ingredient_List.objects.filter(user=uid)]
        isFavorite = favoriteDrink.objects.filter(user=request.user.profile, drink_id=drinkID).exists()
    else:
        isFavorite = False

    if request.method == 'POST':
        if 'newIngredients[]' in request.POST: # User adding new item to their ingredient list
            curr_user = User.objects.get(username=request.user.username)
            newIngredients = request.POST.getlist('newIngredients[]')
            for ingredient in newIngredients:
                newEntry = Ingredient_List.objects.create(user=curr_user, ingredient=ingredient)
                newEntry.save()
        
        if 'isFavorite' in request.POST: # User adding/removing current drink to their favorite drink list
            if request.POST['isFavorite']:
                newFavEntry = favoriteDrink(user=request.user.profile, drink_id=drinkID, drink_name=drinkResult.name)
                newFavEntry.save()
            else:
                previousFavEntry = favoriteDrink.objects.get(user=request.user.profile, drink_id=drinkID, drink_name=drinkResult.name)
                previousFavEntry.delete()

        # Comment and tag form generation
        cform = NewCommentForm(request.POST)
        if cform.is_valid() and "submit_comment" in request.POST:
            comment = Comment.objects.create(message=cform.cleaned_data['message'], 
                user=request.user.profile, drinkID=drinkID)
            comment.save()

        editcform = EditCommentForm(request.POST)
        if editcform.is_valid() and "edit_comment" in request.POST:
            new_message = editcform.cleaned_data['message']
            c_id = editcform.cleaned_data['c_id']
            comment_to_be_changed = Comment.objects.get(id=c_id)
            comment_to_be_changed.message = new_message
            comment_to_be_changed.save()

        tagform = NewTagsForm(request.POST)

        if tagform.is_valid() and "submit_tag" in request.POST:
            tag_string = tagform.cleaned_data['tags']
            tag_list = [x.strip() for x in tag_string.split(',')] # contains parsed tags from user
            tags_of_drink = [i.name for i in Tag.objects.filter(drink_ID=drinkID)] # contains existing tags for drink
            for tag in tag_list:
                # ignore any invalid tags
                if re.match("^[a-zA-Z]*$", tag) and tag not in tags_of_drink:
                    t = Tag.objects.create(name=tag, drink_ID=drinkID)
                    t.save()

        if request.method == "POST" and "radiobutton" in request.POST:
            score = request.POST['radiobutton']
            if drinkRating.objects.filter(drink_id=drinkID, user=request.user.profile).count() != 0:
                rating = drinkRating.objects.get(drink_id=drinkID, user=request.user.profile)
                rating.rating = score
            else:
                rating = drinkRating(drink_id=drinkID, rating=score, user=request.user.profile)
            rating.save()
        
    all_ratings = drinkRating.objects.filter(drink_id=drinkID)
    num_ratings = all_ratings.count()
    if num_ratings > 0:
        avg_rating = 0
        for rating in all_ratings:
            avg_rating += rating.rating
        avg_rating = round(avg_rating / num_ratings, 2)
    else:
        avg_rating = -1

    try:
        user_rating = drinkRating.objects.get(user=request.user.profile, drink_id=drinkID)
    except:
        user_rating = -1

    checked = []
    k = 0
    for i in range(10):
        if avg_rating > k:
            checked.append('checked')
        else:
            checked.append('')
        k += 0.5
    

    comments = Comment.objects.filter(drinkID=drinkID)
    cform = NewCommentForm()
    editcform = EditCommentForm()
    tagform = NewTagsForm()
    
    tags = [i.name for i in Tag.objects.filter(drink_ID=drinkID)]
    
    # #obj = drinkRating(drink_id=Drink.objects.get(cocktaildb_id = drinkID), user=request.user.profile)
    # obj = drinkRating()
    # obj.save()

    
    context = {
        'drink': drinkResult,
        'ingredient_dict': ingredient_dict.items(),
        'user_ingredients': user_ingredients, 
        'comments': comments, 
        'commentform': cform, 
        'recommended_drinks': recommended_drinks, 
        'tagform': tagform,
        'tags': tags,
        'editcform': editcform,
        'isFavorite': isFavorite,
        'average_rating': avg_rating,
        'checkers': checked,
        'user_rating': user_rating
    }
    return render(request, 'DrinkBeyondThePossible/detail.html', context=context)

def results(request):
    drink_results = []
    ingredients = []
    user_ingredients = []

    if 'ingredient' in request.GET: # Get ingredient search parameters from request
        search_results = []
        ingredients = [entry.strip('').lower() for entry in request.GET.getlist('ingredient') if entry]
        
        for ingredient in ingredients:
            #Find every possible drink that can be made from the ingredient
            matching_result = cdb.searchMatchingDrinks(ingredient)
            if isinstance(matching_result, cdb.SearchResult):
                search_results.append(set(matching_result.drinks))
       
        if search_results:
            # Find every drink available from the combination of ingredients
            initial_set = list(search_results)
            comb_chain = itertools.chain.from_iterable(itertools.combinations(initial_set, r) for r in range(1, len(initial_set)+1))
            ingredient_intersections = [set.intersection(*x) for x in comb_chain if set.intersection(*x) != set()]
            drink_results = list({drink for sublist in ingredient_intersections for drink in sublist})
            

    # Retrieve ingredients list of current user if available
    if request.user.is_authenticated:
        user_ingredients = [entry.ingredient for entry in Ingredient_List.objects.filter(user=request.user.id)]

    context = {'drinkResults': drink_results, 'searchIngredients': ingredients, 'userIngredients':user_ingredients}
    return render(request, 'DrinkBeyondThePossible/search_results.html', context=context)

@login_required
def manage(request):
    context = {
        'activePage': 'Account'
    }
    return render(request, 'DrinkBeyondThePossible/account_management.html', context=context)

@login_required
def ingredientList(request):
    if request.method == 'POST':
        if 'delIngredient' in request.POST:
            for ingredient in request.POST.getlist('delIngredient'):
                removedIngredient = Ingredient_List.objects.get(ingredient=ingredient, user=request.user)
                removedIngredient.delete()
        
        if 'ingredient' in request.POST:
            ingredients = [entry.strip('') for entry in request.POST.getlist('ingredient') if entry]

            for ing in ingredients:
                if not Ingredient_List.objects.filter(ingredient=ing, user=request.user).exists():
                    new_ingredient = Ingredient_List(ingredient=ing, user=request.user)
                    new_ingredient.save()
   
    ingredients = Ingredient_List.objects.filter(user=request.user)

    context = {
        'activePage': 'Account',
        'ingredients': ingredients
    }

    return render(request, 'DrinkBeyondThePossible/ingredient_list.html', context=context)

@login_required
def recipeList(request):

    recipes = customDrink.objects.filter(user=request.user.profile)

    if recipes.exists():
        context = {
            'activePage': 'Account',
            'recipes': recipes
        }
    else:
        context = {
            'activePage': 'Account',
            'recipes': []
        }
    return render(request, 'DrinkBeyondThePossible/custom_drinks.html', context=context)

@login_required
def editAccount(request):
    #form = EditAccountForm()
    usernameForm = EditAccountnameForm()
    emailForm = EditEmailForm()
    passwordForm = EditPasswordForm()

    return render(request, 'DrinkBeyondThePossible/edit_account.html', {'usernameForm': usernameForm, 'emailForm': emailForm, 'passwordForm': passwordForm})

@login_required
def editUsername(request):

    if request.method == 'POST':
        form = EditAccountnameForm(request.POST)

        if form.is_valid():
            user = request.user
            user.username=form.cleaned_data['account_name']
            user.save()

    return HttpResponseRedirect('/')

@login_required
def editEmail(request):

    if request.method == 'POST':
        form = EditEmailForm(request.POST)

        if form.is_valid():
            user = request.user
            user.email=form.cleaned_data['email']
            user.save()

    return HttpResponseRedirect('/')

@login_required
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
            username = form.cleaned_data['account_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            return HttpResponseRedirect('/')
    else:
        form = NewAccountForm()

    return render(request, 'DrinkBeyondThePossible/create_account.html', {'form': form})

@login_required
def newCustomDrink(request):
    if request.method == 'POST':
        ingredients = request.POST.getlist('ingredient')

        form = NewDrinkForm(request.POST)
        if form.is_valid(): # Add new drink and entries for its recipe to database
            drink_name = form.cleaned_data['drinkName']
            description = form.cleaned_data['description']
            instructions = form.cleaned_data['instructions']
            #image = form.cleaned_data['image']

            newDrink = customDrink(drink_name=drink_name, description=description, instructions=instructions, user=request.user.profile)
            newDrink.save()
            for ing in ingredients:
                recipeEntry = customRecipe(custom_name=drink_name, user=request.user.profile, ingredient=ing)
                recipeEntry.save()   
    else:
        form = NewDrinkForm()
        
    custom_drinks = []

    if request.user.is_authenticated: # Get custom drinks from logged in user
        custom_drinks = [drink.drink_name for drink in customDrink.objects.filter(user=request.user.profile)]     
    return render(request, 'DrinkBeyondThePossible/new_custom_drink.html', {'form': form, 'customDrinks': custom_drinks})

@login_required
def displayCustomDrinks(request, recipe_name):
    try:
        recipe = customDrink.objects.get(drink_name=recipe_name, user=request.user.profile)
    except Exception as e:
        return HttpResponseRedirect('')

    # Get the corresponding ingredients for this current recipe to pass into context
    ingredients = [r.ingredient for r in customRecipe.objects.filter(user=request.user.profile, custom_name=recipe.drink_name)]

    recipeInfo = {'drinkName': recipe.drink_name, 'description': recipe.description, 'instructions': recipe.instructions, 'image': recipe.image, 'ingredients': ingredients}
    
    user_ingredients = [i.ingredient for i in Ingredient_List.objects.filter(user=request.user)]
    context={'activePage': 'Account', 'recipe': recipeInfo, 'user_ingredients': user_ingredients}
    return render(request, 'DrinkBeyondThePossible/display_custom_drinks.html', context=context)

@login_required
def viewFavoriteDrinks(request):

    getOp = "Favorite Drinks"
    favorites = favoriteDrink.objects.filter(user=request.user.profile)

    if favorites.exists():
        context = {'collection': favorites, 'getOp': getOp}
    else:
        context = {'collection': [], 'getOp': getOp}

    return render(request, 'DrinkBeyondThePossible/display_favorite_drinks.html', context)
