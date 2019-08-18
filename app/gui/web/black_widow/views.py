from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def user(request):
    return render(request, 'user.html')


def tables(request):
    return render(request, 'tables.html')


def typography(request):
    return render(request, 'typography.html')


def icons(request):
    return render(request, 'icons.html')


def notifications(request):
    return render(request, 'notifications.html')
