from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    card = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class State(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.state


class City(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=50)
    state = models.ForeignKey(to=State, related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.city}, {self.state}'


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    city = models.ForeignKey(to=City, related_name='locations', on_delete=models.CASCADE)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Taxi(models.Model):
    id = models.AutoField(primary_key=True)
    driver_name = models.CharField(max_length=50)
    plate = models.CharField(max_length=15)
    model = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    taxi_number = models.IntegerField()
    city = models.ForeignKey(to=City, related_name='taxis', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.taxi_number)


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
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField(null=True, blank=True)
    bus_trip = models.ForeignKey(to=BusTrip, related_name='taxiTrips', on_delete=models.PROTECT)
    user = models.ForeignKey(to=User, related_name='taxiTrips',
                             on_delete=models.PROTECT, null=True, blank=True)
    taxi = models.ForeignKey(to=Taxi, related_name='trips', on_delete=models.PROTECT)
    price = models.FloatField(null=True, blank=True)
    taxi_rating = models.PositiveSmallIntegerField()
    user_rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.id)
