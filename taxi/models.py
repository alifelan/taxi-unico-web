from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    # TODO: tarjeta

    def __str__(self):
        return self.name


class Taxi(models.Model):
    id = models.AutoField(primary_key=True)
    driver_name = models.CharField(max_length=50)
    plate = models.CharField(max_length=15)
    model = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    taxi_number = models.IntegerField()
    busy = models.BooleanField()
    # TODO: ubicacion

    def __str__(self):
        return str(self.taxi_number)


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BusTrip(models.Model):
    id = models.AutoField(primary_key=True)
    origin = models.ForeignKey(to=Location, related_name='busTripsO', on_delete=models.PROTECT)
    destination = models.ForeignKey(to=Location, related_name='busTripsD', on_delete=models.PROTECT)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class TaxiTrip(models.Model):
    id = models.AutoField(primary_key=True)
    origin = models.ForeignKey(to=Location, related_name='taxiTripsO', on_delete=models.PROTECT)
    destination = models.ForeignKey(
        to=Location, related_name='taxiTripsD', on_delete=models.PROTECT)
    date = models.DateTimeField()
    bus_trip = models.ForeignKey(to=BusTrip, related_name='taxiTrips', on_delete=models.PROTECT)
    user = models.ForeignKey(to=User, related_name='taxiTrips', on_delete=models.PROTECT)
    taxi = models.ForeignKey(to=Taxi, related_name='trips', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)
