from multiprocessing import Event
from django.shortcuts import render
from django.http import HttpResponse
from scipy import rand
from .models import Camper, Park, Event, Review, Reservation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import datetime
from django.db.models import Max
from django.http import HttpResponseRedirect
import random


def login(request):
    error_message = ''
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user_password_encrypted = Camper.objects.filter(
                camper_email=email).only('camper_password')[0].camper_password
        except:
            user_password_encrypted = None
        if user_password_encrypted is None:
            error_message = 'Account for this email does not exist'
        else:
            if check_password(password, user_password_encrypted):
                return render(request, 'nationalParks.html')
            else:
                error_message = "Invalid Password"
    return render(request, 'login.html', {'error_message': error_message})


def home(request):
    return render(request, 'home.html')


def parks(request):
    return render(request, 'parks.html')


def nationalParks(request):

    #still need to receive user and park object from parks page#######

    park_list = Park.objects.all().order_by("park_id")
    current_park = park_list[0]

    request.session['park-id'] = current_park.park_id

    camper_list = Camper.objects.all().order_by("camper_id")
    current_camper = camper_list[0]

    ##################################################################

    # Used for testing Different Parks
    # for park in park_list:
    #     if park.park_name == 'Yosemite National Park':
    #         current_park = park
    #     elif park.park_name == 'Yellowstone National Park':
    #         current_park = park
    #     elif park.park_name == 'Glacier National Park':
    #         current_park = park
    #     elif park.park_name == 'Grand Canyon National Park':
    #         current_park = park
    #     elif park.park_name == 'Zion National Park':
    #         current_park = park
    #     elif park.park_name == 'Grand Teton National Park':
    #         current_park = park
    #     elif park.park_name == 'Bryce Canyon National Park':
    #         current_park = park
    #     elif park.park_name == 'Rocky Moutain National Park':
    #         current_park = park
    #     elif park.park_name == 'Arches National Park':
    #         current_park = park
    #     elif park.park_name == 'Great Smoky Mountains National Park':
    #         current_park = park

    event_list = Event.objects.filter(park_id=current_park.park_id)

    if request.method == 'POST':

        newRating = Review()
        newRating.review_rating = request.POST.get('rating-dropdown')
        newRating.review_date = datetime.date.today()
        newRating.review_id = random.randint(0, 999)
        newRating.park = current_park
        newRating.camper = current_camper
        newRating.save()
        return HttpResponseRedirect("")

    return render(request, 'nationalParks.html',
                  {'event_list': event_list, 'current_park': current_park})


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
                newUser = Camper(camper_id=last_id['camper_id__max']+1, camper_email=email, camper_password=make_password(
                    password), camper_registrationdate=datetime.date.today(), camper_name=name)
                newUser.save()
                return render(request, 'home.html')
            except:
                error_message = 'Internal Error. Please try Again.'
    return render(request, 'signup.html', {'error_message': error_message})
