from django.shortcuts import render
from django.http import HttpResponse
from .models import Camper, Park, Event, Review, Reservation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.db.models import Max
from datetime import date, datetime
from django.http import HttpResponseRedirect
import random, math


def login(request, parkID = ""):
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
                request.session['user-id'] = Camper.objects.filter(
                    camper_email=email).only('camper_id')[0].camper_id
                return HttpResponseRedirect('home')
            else:
                error_message = "Invalid Password"
    return render(request, 'login.html', {'error_message': error_message})


def home(request, parkID = ""):
    return render(request, 'home.html')


def parks(request, parkID = ""):

    park_list = Park.objects.all()

    # parkName = request.POST['park-name']

    if request.method == 'POST':

        return HttpResponseRedirect("nationalParks")

    return render(request, 'parks.html',
                  {'park_list': park_list})


def nationalParks(request, parkID):



    #still need to receive user and park object from parks page#######

    park_list = Park.objects.all().order_by("park_id")

    for park in park_list:
        if park.park_id == parkID:
            request.session['park-id'] = park.park_id

    event_list = Event.objects.all()

    review_list = Review.objects.all()

    # current_park = park_list.filter(park_id = parkID)

    camper_list = Camper.objects.all().order_by("camper_id")

    current_camper = camper_list.filter(
        camper_id=request.session['user-id'])[0]

    if request.method == 'POST':
        
        current_park = Park()

        for park in park_list:
            if park.park_id == parkID:
                current_park = park

        for review in review_list:
            if review.park_id == parkID and review.camper == current_camper:
                review.review_rating = request.POST.get('rating-dropdown')
                review.review_date = date.today()
                review.save()
                
        return HttpResponseRedirect("")

    return render(request, 'nationalParks.html',
                {'park_ID': parkID, 'park_list': park_list, 'event_list': event_list, 'review_list': review_list, 'current_camper': current_camper})


def reservations(request, parkID = ""):
    error_message = ''
    if 'park-id' in request.session:
        national_park = Park.objects.filter(
            park_id=request.session['park-id'])[0]
    else:
        national_park = ''
    estimated_cost = ''
    reservations = ''
    start_date = None
    end_date = None
    if request.method == "POST":
        try:
            start_date = datetime.strptime(
                request.POST['start-date'], '%m/%d/%Y')
            end_date = datetime.strptime(request.POST['end-date'], '%m/%d/%Y')
        except:
            error_message = "Invalid date format. Try Again."
            return render(request, 'reservations.html', {'national_park': national_park.park_name, 'error_message': error_message, 'estimated_cost': estimated_cost})
        try:
            time_delta = end_date - start_date
            if time_delta.days < 0:
                raise Exception("Start and End dates are not valid.")
        except:
            error_message = 'Incompatible Start and End Dates.'
            return render(request, 'reservations.html', {'national_park': national_park.park_name, 'error_message': error_message, 'estimated_cost': estimated_cost})
        try:
            last_id = Reservation.objects.aggregate(Max('reservation_id'))
            if last_id['reservation_id__max'] == None:
                last_id['reservation_id__max'] = 0
            time_delta = end_date - start_date

            cost = national_park.park_sevendaycost * math.ceil(time_delta.days / 7)

            estimated_cost = cost
            newReservation = Reservation(
                park=national_park,
                camper=Camper.objects.filter(
                    camper_id=request.session['user-id'])[0],
                reservation_id=last_id['reservation_id__max']+1,
                reservation_startdate=start_date,
                reservation_enddate=end_date,
                reservation_totalcost=cost)
            newReservation.save()
        except:
            error_message = 'Internal Error. Please try again.'
    try:
        reservations = Reservation.objects.filter(camper=Camper.objects.filter(camper_id=request.session['user-id'])[0],
                                                  park=national_park)
    except:
        error_message = 'Could not get your reservations.'
    return render(request, 'reservations.html', {'national_park': national_park.park_name, 'error_message': error_message, 'estimated_cost': estimated_cost, 'reservations': reservations})

def updateReservations(request, reservationID):
    if 'park-id' in request.session:
        national_park = Park.objects.filter(
            park_id=request.session['park-id'])[0]
    reservationList = Reservation.objects.filter(camper=Camper.objects.filter(camper_id=request.session['user-id'])[0],
                                                  park=national_park)
    updateMessage = ''
    deleteMessage = ''
    if request.method == "POST":
        thisReservation_id = request.POST['reservation-id']
        start_date = datetime.strptime(request.POST['start-date'], '%m/%d/%Y')
        end_date = datetime.strptime(request.POST['end-date'], '%m/%d/%Y')
        reservationToEdit = Reservation.objects.filter(reservation_id=int(thisReservation_id))[0]
        if start_date.strftime('%m/%d/%Y') == reservationToEdit.reservation_startdate.strftime('%m/%d/%Y') and end_date.strftime('%m/%d/%Y') == reservationToEdit.reservation_enddate.strftime('%m/%d/%Y'):
            #delete reservation
            Reservation.objects.filter(reservation_id=int(thisReservation_id))[0].delete()
            deleteMessage = 'Reservation deleted successfully'
            #return render(request,'updateReservations.html', {'reservationID': reservationID, 'reservationList': reservationList, 'message':message})
            return render(request,'reservations.html', {'deleteMessage':deleteMessage,'national_park':national_park.park_name, 'reservations': Reservation.objects.filter(camper=Camper.objects.filter(camper_id=request.session['user-id'])[0],park=national_park) })
        else:
            #update reservation
            reservationToEdit.reservation_startdate = start_date
            reservationToEdit.reservation_enddate = end_date
            time_delta = end_date - start_date
            if time_delta.days <= 0:
                return render(request, 'updateReservations.html', {'reservationID': reservationID, 'reservationList': reservationList, 'error_message': 'Invalid Dates. Try Again.'})
            reservationToEdit.reservation_totalcost = national_park.park_sevendaycost * math.ceil(time_delta.days / 7)
            #reservationToEdit.reservation_totalcost 
            reservationToEdit.save()
            updateMessage = 'Reservation updated successfully. New Total: $' + str(national_park.park_sevendaycost * math.ceil(time_delta.days / 7))
            return render(request,'reservations.html', {'updateMessage':updateMessage, 'national_park':national_park.park_name, 'reservations':Reservation.objects.filter(camper=Camper.objects.filter(camper_id=request.session['user-id'])[0],park=national_park)})
        #return render(request,'updateReservations.html', {'reservationID': reservationID, 'reservationList': reservationList, 'datesMatch': datesMatch, 'tsd':tsd, 'sd':start_date})
    return render(request, 'updateReservations.html', {'reservationID': reservationID, 'reservationList': reservationList})


def signup(request, parkID = ""):
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
                    password), camper_registrationdate=date.today(), camper_name=name)
                newUser.save()
                request.session['user-id'] = Camper.objects.filter(
                    camper_email=email).only('camper_id')[0].camper_id
                return HttpResponseRedirect('home')
            except:
                error_message = 'Internal Error. Please try Again.'
    return render(request, 'signup.html', {'error_message': error_message})

