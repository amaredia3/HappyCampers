from django.contrib import admin
from app.models import Park, Event, Camper, Reservation, Review
# Register your models here.

admin.site.register(Park)
admin.site.register(Event)
admin.site.register(Camper)
admin.site.register(Reservation)
admin.site.register(Review)
