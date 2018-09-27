from django.shortcuts import render

# Create your views here.
def index(request):
    context = {'activePage': 'Home'}
    return render(request, 'DrinkBeyondThePossible/home.html', context=context)

def detail(request):
    context = {}
    return render(request, 'DrinkBeyondThePossible/detail.html', context=context)

def results(request):
    drinkResults = {'Test 1', 'Test 2'}

    context = {'drinkResults': drinkResults}
    return render(request, 'DrinkBeyondThePossible/search_results.html', context=context)