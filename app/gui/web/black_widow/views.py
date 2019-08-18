from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def tables(request):
    return render(request, 'tables.html')


def user(request):
    return render(request, 'user.html')
