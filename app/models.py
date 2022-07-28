from django.db import models


class Camper(models.Model):
    camper_id = models.IntegerField(primary_key=True)
    camper_password = models.CharField(max_length=-1, blank=True, null=True)
    camper_email = models.CharField(max_length=-1, blank=True, null=True)
    camper_registrationdate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camper'


class Park(models.Model):
    park_id = models.IntegerField(primary_key=True)
    park_name = models.CharField(max_length=-1, blank=True, null=True)
    park_state = models.CharField(max_length=-1, blank=True, null=True)
    park_coordinates = models.CharField(max_length=-1, blank=True, null=True)
    park_description = models.CharField(max_length=-1, blank=True, null=True)
    park_avgrating = models.FloatField(blank=True, null=True)
    park_numreviews = models.IntegerField(blank=True, null=True)
    park_sevendaycost = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'park'


class Reservation(models.Model):
    reservation_id = models.IntegerField(primary_key=True)
    camper = models.ForeignKey(
        Camper, models.DO_NOTHING, blank=True, null=True)
    park = models.ForeignKey(Park, models.DO_NOTHING, blank=True, null=True)
    reservation_startdate = models.DateField(blank=True, null=True)
    reservation_enddate = models.DateField(blank=True, null=True)
    reservation_totalcost = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservation'


class Review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    camper = models.ForeignKey(
        Camper, models.DO_NOTHING, blank=True, null=True)
    park = models.ForeignKey(Park, models.DO_NOTHING, blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    review_rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'
