from django.urls import path
from . import views
urlpatterns = [
path('', views.login, name='login'),
path('home',views.home, name='home'),
path('parks',views.parks, name='parks'),
path('reservations',views.reservations, name='reservations'),
path('nationalParks',views.nationalParks, name='nationalParks'),
path('signup',views.signup, name='signup'),
]