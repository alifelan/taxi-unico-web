from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from taxi.models import Taxi, User, Location, BusTrip, TaxiTrip
from taxi.serializers import TaxiSerializer, UserSerializer, LocationSerializer, BusTripSerializer, TaxiTripSerializer
from datetime import datetime
from random import randint
import json

# Create your views here.


@csrf_exempt
def user(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        name = body['name']
        email = body['email']
        password = body['password']
        if len(User.objects.filter(email=email)) > 0:
            return JsonResponse({'status': 'false', 'message': 'User already exists. Use put to update'}, status=200)
        card = body['card']
        user = User(name=name, email=email, password=password, card=card)
        user.save()
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        body = json.loads(request.body.decode("utf-8"))
        user_email = body['email']
        try:
            user = User.objects.get(email=user_email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        name = user.name
        password = user.password
        for key in body.keys():
            if key == 'name':
                name = body[key]
            elif key == 'password':
                password = body[key]
        user = User(name=name, email=user_email, password=password)
        user.save()
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)


def login(request):
    if request.method == 'GET':
        body = json.loads(request.body.decode("utf-8"))
        user_email = body['email']
        try:
            user = User.objects.get(email=user_email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        user_password = body['password']
        if user.password == user_password:
            return JsonResponse({'status': 'true', 'message': 'Success on loging in'}, status=200)
        return JsonResponse({'status': 'false', 'message': 'Wrong password'}, status=403)


def get_user_taxi_trips(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        body = json.loads(request.body.decode("utf-8"))
        user_email = body['email']
        try:
            user = User.objects.get(email=user_email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        user_taxi_trips = user.taxiTrips.all()
        serializer = TaxiTripSerializer(user_taxi_trips, many=True)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only get'}, status=404)


@csrf_exempt
def create_taxi_trip(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        origin_name = body['originName']
        origin_state = body['originState']
        origin_city = body['originCity']
        origin_address = body['originAddress']
        try:
            origin = Location.objects.get(
                name=origin_name, state=origin_state, city=origin_city, address=origin_address)
        except ObjectDoesNotExist:
            origin = Location(name=origin_name, state=origin_state,
                              city=origin_city, address=origin_address)
            origin.save()
        destination_name = body['destinationName']
        destination_state = body['destinationState']
        destination_city = body['destinationCity']
        destination_address = body['destinationAddress']
        try:
            destination = Location.objects.get(
                name=destination_name, state=destination_state, city=destination_city, address=destination_address)
        except ObjectDoesNotExist:
            destination = Location(name=destination_name, state=destination_state,
                                   city=destination_city, address=destination_address)
            destination.save()
        date = datetime.now()
        if 'date' in body:
            date = datetime.strptime(body['date'], '%m/%d/%y %H:%M')
        bus_trip_id = body['busTripId']
        try:
            bus_trip = BusTrip.objects.get(id=bus_trip_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Bus trip does not exist'}, status=404)
        # TODO: Este pedo puede ser nulo
        user_email = body['userEmail']
        try:
            user = User.objects.get(email=user_email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        # TODO: taxis agarrado de la base segun el tiempo en el que esten libres
        # aka checar que no esten en un viaje a la hora de inicio de este viaje
        taxi_id = body['taxiId']
        try:
            taxi = Taxi.objects.get(id=taxi_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Taxi does not exist'}, status=404)
        taxi_trip = TaxiTrip(origin=origin, destination=destination, date=date,
                             bus_trip=bus_trip, user=user, taxi=taxi)
        taxi_trip.save()
        serializer = TaxiTripSerializer(taxi_trip)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def bus_trip(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        origin_name = body['originName']
        origin_state = body['originState']
        origin_city = body['originCity']
        origin_address = body['originAddress']
        try:
            origin = Location.objects.get(
                name=origin_name, state=origin_state, city=origin_city, address=origin_address)
        except ObjectDoesNotExist:
            origin = Location(name=origin_name, state=origin_state,
                              city=origin_city, address=origin_address)
            origin.save()
        destination_name = body['destinationName']
        destination_state = body['destinationState']
        destination_city = body['destinationCity']
        destination_address = body['destinationAddress']
        try:
            destination = Location.objects.get(
                name=destination_name, state=destination_state, city=destination_city, address=destination_address)
        except ObjectDoesNotExist:
            destination = Location(name=destination_name, state=destination_state,
                                   city=destination_city, address=destination_address)
            destination.save()
        date = datetime.now()
        if 'date' in body:
            date = datetime.strptime(body['date'], '%m/%d/%y %H:%M')
        bus_trip = BusTrip(origin=origin, destination=destination,
                           departure_date=date, arrival_date=date)
        serializer = BusTripSerializer(bus_trip)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'GET':
        body = json.loads(request.body.decode("utf-8"))
        bus_id = body['id']
        try:
            bus_trip = BusTrip.objects.get(id=bus_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Bus trip does not exist'}, status=404)
        serializer = BusTripSerializer(bus_trip)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'status': 'false', 'message': 'Only get'}, status=404)


def get_random_bus_trip(request):
    if request.method == 'GET':
        bus_trip_id = randint(1, len(BusTrip.objects.all()))
        try:
            bus_trip = BusTrip.objects.get(id=bus_trip_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'There are no bus trips'}, status=404)
        serializer = BusTripSerializer(bus_trip)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only get'}, status=404)
