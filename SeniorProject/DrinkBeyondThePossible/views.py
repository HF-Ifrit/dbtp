from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'DrinkBeyondThePossible/home.html', {})

def detail(request):
    return render(request, 'DrinkBeyondThePossible/detail.html', {})