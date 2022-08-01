from distutils.log import error
from multiprocessing import Event
from django.shortcuts import render
from django.http import HttpResponse
from .models import Camper, Park, Event, Review, Reservation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import datetime
from django.db.models import Max
from datetime import datetime

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
                request.session['user-id'] = Camper.objects.filter(camper_email=email).only('camper_id')[0].camper_id
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

    request.session['park-id'] = park_list[0].park_id

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
    error_message = ''
    if 'park-id' in request.session:
        national_park = Park.objects.filter(park_id=request.session['park-id'])[0]
    else:
        national_park = ''
    estimated_cost = ''
    reservations = ''
    start_date = None
    end_date = None
    if request.method == "POST":
        try:
            start_date = datetime.strptime(request.POST['start-date'], '%m/%d/%Y')
            end_date = datetime.strptime(request.POST['end-date'],'%m/%d/%Y')
        except:
            error_message = "Invalid date format. Try Again."
            return render(request, 'reservations.html', { 'national_park': national_park.park_name, 'error_message': error_message, 'estimated_cost': estimated_cost})
        try:
            time_delta = end_date - start_date
            if time_delta.days < 0:
                raise Exception("Start and End dates are not valid.")
        except:
            error_message = 'Incompatible Start and End Dates.'
            return render(request, 'reservations.html', { 'national_park': national_park.park_name, 'error_message': error_message, 'estimated_cost': estimated_cost})
        try:
            last_id = Reservation.objects.aggregate(Max('reservation_id'))
            if last_id['reservation_id__max'] == None:
                last_id['reservation_id__max'] = 0
            time_delta = end_date - start_date
            cost = national_park.park_sevendaycost * (time_delta.days / 7.0)
            estimated_cost = cost
            newReservation = Reservation(
                                            park=national_park,
                                            camper=Camper.objects.filter(camper_id=request.session['user-id'])[0],
                                            reservation_id=last_id['reservation_id__max']+1,
                                            reservation_startdate=start_date,
                                            reservation_enddate = end_date,
                                            reservation_totalcost=cost)
            newReservation.save()
        except:
            error_message = 'Internal Error. Please try again.'
    try:
        reservations = Reservation.objects.filter(camper=Camper.objects.filter(camper_id=request.session['user-id'])[0],
                                                park=national_park)
    except:
        error_message = 'Could not get your reservations.'
    return render(request, 'reservations.html', { 'national_park': national_park.park_name, 'error_message': error_message, 'estimated_cost': estimated_cost, 'reservations': reservations})


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
                request.session['user-id'] = Camper.objects.filter(camper_email=email).only('camper_id')[0].camper_id
                return render(request,'home.html')
            except:
                error_message = 'Internal Error. Please try Again.'
    return render(request, 'signup.html', {'error_message': error_message})
