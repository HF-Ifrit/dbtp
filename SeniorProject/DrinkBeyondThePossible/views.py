from django.shortcuts import render
from .forms import EditAccountForm
from .forms import NewAccountForm
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User

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


def editAccount(request):

    if request.method == 'POST':
        form = EditAccountForm(request.POST)


        if form.is_valid():

        # do account change stuff
            user = request.user
            user.username=form.cleaned_data['account_name']
            user.save()
            user.set_password(form.cleaned_data['password'])
            user.save()

            return HttpResponseRedirect('')

    else:
        form = EditAccountForm()

    return render(request, 'DrinkBeyondThePossible/edit_account.html', {'form': form})


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


