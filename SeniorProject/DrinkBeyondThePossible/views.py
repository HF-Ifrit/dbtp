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
from .forms import NewDrinkForm

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
        drinkResults = request.GET.getlist('ingredient')
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

# def newCustomDrink(request):
#     context = {
#         'activePage': 'Account'
#     }
#     return render(request, 'DrinkBeyondThePossible/new_custom_drink.html', context=context)

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
