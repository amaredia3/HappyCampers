from multiprocessing import Event
from django.shortcuts import render
from django.http import HttpResponse
from .models import Park
from .models import Event


def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def parks(request):
    return render(request, 'parks.html')


def nationalParks(request):
    park_list = Park.objects.filter(park_name='Yosemite National Park')
    event_list = Event.objects.filter(park_id='1')
    return render(request, 'nationalParks.html',
                  {'park_list': park_list,
                   'event_list': event_list})


def reservations(request):
    return render(request, 'reservations.html')


def signup(request):
    return render(request, 'signup.html')
