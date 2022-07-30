from multiprocessing import Event
from django.shortcuts import render
from django.http import HttpResponse
from .models import Camper, Park, Event, Review, Reservation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import datetime
from django.db.models import Max

def login(request):
    error_message = ''
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user_password_encrypted = Camper.objects.filter(camper_email=email).only('camper_password')[0].camper_password
        except:
            user_password_encrypted = None
        if user_password_encrypted is None:
            error_message = 'Account for this email does not exist'
        else:
            if check_password(password,user_password_encrypted):
                return render(request, 'home.html')
            else:
                error_message = "Invalid Password"
    return render(request, 'login.html', {'error_message': error_message})


def home(request):
    return render(request, 'home.html')


def parks(request):
    return render(request, 'parks.html')


def nationalParks(request):

    park_list = Park.objects.filter(park_name='Yosemite National Park')
    event_list = Event.objects.filter(park_id='1')

    if request.method == 'POST':
        newRating = Review()
        newRating.review_rating = request.POST.get('rating-dropdown')
        newRating.review_id = 1
        newRating.save()

        return render(request, 'nationalParks.html',
                      {'park_list': park_list,
                       'event_list': event_list})

    else:
        return render(request, 'nationalParks.html',
                      {'park_list': park_list,
                       'event_list': event_list})


def reservations(request):
    return render(request, 'reservations.html')


def signup(request):
    error_message = ''
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        if Camper.objects.filter(camper_email=email).exists():
            error_message = 'Account for this email already exists'
        else:
            last_id = Camper.objects.aggregate(Max('camper_id'))
            try:
                newUser = Camper(camper_id=last_id['camper_id__max']+1,camper_email=email,camper_password=make_password(password),camper_registrationdate=datetime.date.today(),camper_name=name)
                newUser.save()
                return render(request,'home.html')
            except:
                error_message = 'Internal Error. Please try Again.'
    return render(request, 'signup.html', {'error_message': error_message})
