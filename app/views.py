from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def parks(request):
    return render(request, 'parks.html')

def nationalParks(request):
    return render(request, 'nationalParks.html')

def reservations(request):
    return render(request, 'reservations.html')

def signup(request):
    return render(request, 'signup.html')