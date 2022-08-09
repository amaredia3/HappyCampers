from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Camper, Park, Event, Review, Reservation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.db.models import Max
from datetime import date, datetime
from django.http import HttpResponseRedirect
import random, math


def login(request, parkID = ""):
    """
    This function manages the login form on the login page. Read from Camper Entity.
    """
    error_message = ''
    #if a post form
    if request.method == "POST":
        #get emaill and password from request
        email = request.POST['email']
        password = request.POST['password']
        try:
            #check to see if an account for this email exists.
            user_password_encrypted = Camper.objects.filter(
                camper_email=email).only('camper_password')[0].camper_password
        except:
            user_password_encrypted = None
        if user_password_encrypted is None:
            #set error message if account does not exist
            error_message = 'Account for this email does not exist'
        else:
            #if account exists validate password
            if check_password(password, user_password_encrypted):
                request.session['user-id'] = Camper.objects.filter(
                    camper_email=email).only('camper_id')[0].camper_id
                return HttpResponseRedirect('home')
            else:
                #if incorrect password
                error_message = "Invalid Password"
    return render(request, 'login.html', {'error_message': error_message})


def home(request, parkID = ""):
    if request.method == 'POST':
        Camper.objects.filter(camper_id=request.session['user-id'])[0].delete()
        return HttpResponseRedirect("signup")
    return render(request, 'home.html')


def parks(request, parkID = ""):

    park_list = Park.objects.all()

    # parkName = request.POST['park-name']

    if request.method == 'POST':

        return HttpResponseRedirect("nationalParks")

    return render(request, 'parks.html',
                  {'park_list': park_list})


#view for the national parks page
def nationalParks(request, parkID):

    #creates park list
    park_list = Park.objects.all().order_by("park_id")

    #finds selected park
    for park in park_list:
        if park.park_id == parkID:
            request.session['park-id'] = park.park_id

    #creates event list
    event_list = Event.objects.all()

    #creates review list
    review_list = Review.objects.all()

    #creates camper list
    camper_list = Camper.objects.all().order_by("camper_id")

    #finds current user
    current_camper = camper_list.filter(
        camper_id=request.session['user-id'])[0]

    #checks if review is submitted/updated
    if request.method == 'POST':
        
        #bool to check if button click was for new review
        newReview = True

        #finds current park
        current_park = Park()

        for park in park_list:
            if park.park_id == parkID:
                current_park = park

        if "delete" in request.POST.values(): # delete review
            Review.objects.filter(review_id = 'delete_id').delete()
        else:
            for review in review_list:
                if review.park_id == parkID and review.camper == current_camper: # update review
                    newReview = False
                    review.review_rating = request.POST.get('rating-dropdown')
                    review.review_date = date.today()
                    review.save()

            if newReview == True: # create review
                newRating = Review()
                newRating.review_rating = request.POST.get('rating-dropdown')
                newRating.review_date = date.today()
                newRating.review_id = random.randint(0, 999)
                newRating.park = current_park
                newRating.camper = current_camper
                newRating.save()
                
            review_list = Review.objects.all()
        
        park_list = Park.objects.all().order_by("park_id")

    #renders view with appropriate objects
    return render(request, 'nationalParks.html',
                {'park_ID': parkID, 'park_list': park_list, 'event_list': event_list, 'review_list': review_list, 'current_camper': current_camper})

def reservations(request, parkID = ""):
    """
    This function handles the reservations form on the reservations page. Create and Read on reservation entity.
    """
    error_message = ''
    #get park name from session variable
    if 'park-id' in request.session:
        national_park = Park.objects.filter(
            park_id=request.session['park-id'])[0]
    else:
        national_park = ''
    estimated_cost = ''
    reservations = ''
    start_date = None
    end_date = None
    #get all reservations for camper currently logged in
    reservations = Reservation.objects.filter(camper=Camper.objects.filter(camper_id=request.session['user-id'])[0],
                                                  park=national_park)
    if request.method == "POST":
        try:
            #get users date inputs and format to datetime
            start_date = datetime.strptime(
                request.POST['start-date'], '%m/%d/%Y')
            end_date = datetime.strptime(request.POST['end-date'], '%m/%d/%Y')
        except:
            #set error is invalid date format
            error_message = "Invalid date format. Try Again."
            return render(request, 'reservations.html', {'national_park': national_park.park_name, 'error_message': error_message, 'estimated_cost': estimated_cost,'reservations': reservations})
        try:
            #check to make sure start date falls before the end date
            time_delta = end_date - start_date
            if time_delta.days < 0:
                raise Exception("Start and End dates are not valid.")
        except:
            #throw error if end date occurs before start date
            error_message = 'Incompatible Start and End Dates.'
            return render(request, 'reservations.html', {'national_park': national_park.park_name, 'error_message': error_message, 'estimated_cost': estimated_cost,'reservations': reservations})
        try:
            #calculate cost for the reservation
            last_id = Reservation.objects.aggregate(Max('reservation_id'))
            if last_id['reservation_id__max'] == None:
                last_id['reservation_id__max'] = 0
            time_delta = end_date - start_date

            cost = national_park.park_sevendaycost * math.ceil(time_delta.days / 7)

            estimated_cost = cost
            #create and save the new reservation
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
            #set internal error in case of DB failure
            error_message = 'Internal Error. Please try again.'
    try:
        reservations = Reservation.objects.filter(camper=Camper.objects.filter(camper_id=request.session['user-id'])[0],
                                                  park=national_park)
    except:
        #set error if cannot get reservations for the current camper
        error_message = 'Could not get your reservations.'
    return render(request, 'reservations.html', {'national_park': national_park.park_name, 'error_message': error_message, 'estimated_cost': estimated_cost, 'reservations': reservations})


def updateReservations(request, reservationID):
    """
    This function handled the update reservation form on updateReservations page. Update and Delete on Reservation entity.
    """
    if 'park-id' in request.session:
        #get park for which reservation is being modified
        national_park = Park.objects.filter(
            park_id=request.session['park-id'])[0]
    reservationList = Reservation.objects.filter(camper=Camper.objects.filter(camper_id=request.session['user-id'])[0],
                                                  park=national_park)
    updateMessage = ''
    deleteMessage = ''
    #if post request
    if request.method == "POST":
        #get user entered dates
        thisReservation_id = request.POST['reservation-id']
        start_date = datetime.strptime(request.POST['start-date'], '%m/%d/%Y')
        end_date = datetime.strptime(request.POST['end-date'], '%m/%d/%Y')
        #get reservation we want to edit
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
            #update reservation dates and save
            reservationToEdit.save()
            updateMessage = 'Reservation updated successfully. New Total: $' + str(national_park.park_sevendaycost * math.ceil(time_delta.days / 7))
            return render(request,'reservations.html', {'updateMessage':updateMessage, 'national_park':national_park.park_name, 'reservations':Reservation.objects.filter(camper=Camper.objects.filter(camper_id=request.session['user-id'])[0],park=national_park)})
        #return render(request,'updateReservations.html', {'reservationID': reservationID, 'reservationList': reservationList, 'datesMatch': datesMatch, 'tsd':tsd, 'sd':start_date})
    return render(request, 'updateReservations.html', {'reservationID': reservationID, 'reservationList': reservationList})


def signup(request, parkID = ""):
    """
    This function handles the signup form on the signup page. Create on camper entity.
    """
    error_message = ''
    #if post request
    if request.method == "POST":
        # get user input fields
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        if Camper.objects.filter(camper_email=email).exists():
            #set error message if account for this email already exists
            error_message = 'Account for this email already exists'
        else:
            last_id = Camper.objects.aggregate(Max('camper_id'))
            try:
                #if account does not already exist create a new camper account
                newUser = Camper(camper_id=last_id['camper_id__max']+1, camper_email=email, camper_password=make_password(
                    password), camper_registrationdate=date.today(), camper_name=name)
                newUser.save()
                #set new account as a session variable to be accessible from other pages.
                request.session['user-id'] = Camper.objects.filter(
                    camper_email=email).only('camper_id')[0].camper_id
                return HttpResponseRedirect('home')
            except:
                #set internal error if it is a DB failure
                error_message = 'Internal Error. Please try Again.'
    return render(request, 'signup.html', {'error_message': error_message})

def changePassword(request):
    '''
    This function handles the change password form from changePassword.html. 
    Receives from POST request: email, current password, and new password.
    Then, tries to hash inputted current password and verifies account exists
    Then it verifies the current password is correct then edits the password.
    '''
    error_message = ''
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        newPassword = request.POST['newPassword']
        try:
            hashed_password = Camper.objects.filter(
                camper_email=email).only('camper_password')[0].camper_password
        except:
            hashed_password = None
        if hashed_password is None:
            error_message = 'Account for this email does not exist'
        else:
            if check_password(password, hashed_password):
                user = Camper.objects.filter(camper_email=email).only('camper_id')[0]
                user.camper_password = str(make_password(newPassword))
                user.save()
                return HttpResponseRedirect('home')
            else:
                error_message = "Invalid Password"
    return render(request, 'changePassword.html', {'error_message': error_message})

def logout(request):
    '''
    Delete session and redirect to login page.
    '''
    try:
        del request.session['user']
    except:
        return redirect('login')
    return redirect('login')
