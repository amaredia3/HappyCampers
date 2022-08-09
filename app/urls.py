from django.urls import path
from . import views
urlpatterns = [
    path('', views.login, name='login'),
    path('home',views.home, name='home'),
    path('parks',views.parks, name='parks'),
    path('reservations',views.reservations, name='reservations'),
    path('updateReservations/<int:reservationID>/',views.updateReservations, name='updateReservations'),
    path('nationalParks/<int:parkID>/',views.nationalParks, name='nationalParks'),
    path('signup',views.signup, name='signup'),
    path('changePassword',views.changePassword, name='changePassword'),
    path('logout',views.logout, name='logout')
]