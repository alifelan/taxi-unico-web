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
    """
    user works with POST and PUT,

    POST:
        Receives a json with data te create a user.
        Param:
            name: User name
            email: User email
            password: User password
        Status:
            400: Missing data in json
            405: User exists, use PUT to update data
        Returns: User
            {
                name, email
            }

    PUT:
        Updates user with data received in json
        Param:
            email: User email
            name (optional): New name
            password (optional): New password
            card: Credit card
        Status:
            400: Missing data in json
            404: User does not exist
        Returns: User
            {
                name, email
            }
    """
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        try:
            name = body['name']
            email = body['email']
            password = body['password']
            card = body['card']
        except:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        if len(User.objects.filter(email=email)) > 0:
            return JsonResponse({'status': 'false', 'message': 'User already exists. Use put to update'}, status=405)
        user = User(name=name, email=email, password=password, card=card)
        user.save()
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        body = json.loads(request.body.decode("utf-8"))
        try:
            user_email = body['email']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
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
    return JsonResponse({'status': 'false', 'message': 'Only POST and PUT'}, status=405)


def login(request):
    """
    Login checks email and password received
    Param:
        email: User email
        password: User password
    Status:
        400: Missing data in json
        404: User email does not exist
        200: Success
        403: Wrong password
        405: Wrong method
    Returns:
        {status, message}
    """
    if request.method == 'GET':
        body = json.loads(request.body.decode("utf-8"))
        try:
            user_email = body['email']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        try:
            user = User.objects.get(email=user_email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        user_password = body['password']
        if user.password == user_password:
            return JsonResponse({'status': 'true', 'message': 'Success on loging in'}, status=200)
        return JsonResponse({'status': 'false', 'message': 'Wrong password'}, status=403)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


def get_user_taxi_trips(request):
    """
    Returns taxi trips of a user
    Param:
        email: user email
    Status:
        400: Missing data in json
        404: User does not exist
        405: Wrong method
    Returns: [TaxiTrip]
        [{
            id, origin: {id, name, state, city, address}, destination: {id,
            name, state, city, address}, date, bus_trip: {id, origin: {id, name,
            state, city, address}, destination: {id, name, state, city,
            address}, departure_date, arrival_date}, user: {name, email},
            taxi: {id, driver_name, plate, model, brand, taxi_number}
        }]
    """
    if request.method == 'GET':
        body = json.loads(request.body.decode("utf-8"))
        try:
            user_email = body['email']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        try:
            user = User.objects.get(email=user_email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        user_taxi_trips = user.taxiTrips.all()
        serializer = TaxiTripSerializer(user_taxi_trips, many=True)
        response = {"data": serializer.data}
        return JsonResponse(response, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


@csrf_exempt
def create_taxi_trip(request):
    """
    Creates a taxi trip with data received
    Param:
        origin: Origin data
            name: Name
            state: State
            city: City
            address: Address
        destionation: Destination data
            name: Name
            state: State
            city: City
            address: Address
        date: Date and time of the trip, in format Month/Day/Year Hour:Minutes
        busTripId: Identifier of the bus trip
        userEmail (optional): user email
    Status:
        400: Missing data in json
        404: User or bus trip does not exist
        403: All taxis are busy
        405: Wrong method
    Returns: TaxiTrip
        {
            id, origin: {id, name, state, city, address}, destination: {id,
            name, state, city, address}, date, bus_trip: {id, origin: {id, name,
            state, city, address}, destination: {id, name, state, city,
            address}, departure_date, arrival_date}, user: {name, email},
            taxi: {id, driver_name, plate, model, brand, taxi_number}
        }
    """
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        try:
            origin_json = json['origin']
            origin_name = origin_json['name']
            origin_state = origin_json['state']
            origin_city = origin_json['city']
            origin_address = origin_json['address']
            destination_json = body['destination']
            destination_name = destination_json['name']
            destination_state = destination_json['state']
            destination_city = destination_json['city']
            destination_address = destination_json['address']
            date = datetime.now()
            if 'date' in body:
                date = datetime.strptime(body['date'], '%m/%d/%y %H:%M')
            bus_trip_id = body['busTripId']
            user: User
            try:
                user_email = body['userEmail']
                try:
                    user = User.objects.get(email=user_email)
                except ObjectDoesNotExist:
                    return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
            except KeyError:
                user = None
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        try:
            origin = Location.objects.get(
                name=origin_name, state=origin_state, city=origin_city, address=origin_address)
        except ObjectDoesNotExist:
            origin = Location(name=origin_name, state=origin_state,
                              city=origin_city, address=origin_address)
            origin.save()
        try:
            destination = Location.objects.get(
                name=destination_name, state=destination_state, city=destination_city, address=destination_address)
        except ObjectDoesNotExist:
            destination = Location(name=destination_name, state=destination_state,
                                   city=destination_city, address=destination_address)
            destination.save()
        try:
            bus_trip = BusTrip.objects.get(id=bus_trip_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Bus trip does not exist'}, status=404)
        trips = TaxiTrip.objects.filter(date=date)
        busy_taxis = {trip.taxi for trip in trips}
        free_taxis = set(Taxi.objects.all()) - busy_taxis
        taxi: Taxi
        if len(free_taxis) > 0:
            taxi = list(free_taxis)[0]
        else:
            return JsonResponse({'status': 'false', 'message': 'All taxis are busy at that time'}, status=403)
        taxi_trip = TaxiTrip(origin=origin, destination=destination, date=date,
                             bus_trip=bus_trip, user=user, taxi=taxi)
        taxi_trip.save()
        serializer = TaxiTripSerializer(taxi_trip)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only POST'}, status=405)


@csrf_exempt
def bus_trip(request):
    """
    Works with POST and GET

    POST:
    Creates bus trip
    Param:
        origin: Origin data
            name: Name
            state: State
            city: City
            address: Address
        destionation: Destination data
            name: Name
            state: State
            city: City
            address: Address
        date: Date and time of the trip, in format Month/Day/Year Hour:Minutes
    Status:
        400: Missing data in json
        404: User or bus trip does not exist
        403: All taxis are busy
        405: Wrong method
    Returns: BusTrip
        {
            id, origin: {id, name, state, city, address}, destination: {id,
            name, state, city, address}, departure_date, arrival_date
        }

    GET:
    Gets bus trip
    Param:
        id: Bus trip id
    Status:
        400: Missing field
        404: Bus trip with id doesnt exist
    Returns: BusTrip
        {
            id, origin: {id, name, state, city, address}, destination: {id,
            name, state, city, address}, departure_date, arrival_date
        }
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode("utf-8"))
            origin_json = json['origin']
            origin_name = origin_json['name']
            origin_state = origin_json['state']
            origin_city = origin_json['city']
            origin_address = origin_json['address']
            destination_json = body['destination']
            destination_name = destination_json['name']
            destination_state = destination_json['state']
            destination_city = destination_json['city']
            destination_address = destination_json['address']
            date = datetime.now()
            if 'date' in body:
                date = datetime.strptime(body['date'], '%m/%d/%y %H:%M')
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        try:
            origin = Location.objects.get(
                name=origin_name, state=origin_state, city=origin_city, address=origin_address)
        except ObjectDoesNotExist:
            origin = Location(name=origin_name, state=origin_state,
                              city=origin_city, address=origin_address)
            origin.save()
        try:
            destination = Location.objects.get(
                name=destination_name, state=destination_state, city=destination_city, address=destination_address)
        except ObjectDoesNotExist:
            destination = Location(name=destination_name, state=destination_state,
                                   city=destination_city, address=destination_address)
            destination.save()
        bus_trip = BusTrip(origin=origin, destination=destination,
                           departure_date=date, arrival_date=date)
        serializer = BusTripSerializer(bus_trip)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'GET':
        body = json.loads(request.body.decode("utf-8"))
        try:
            bus_id = body['id']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing id'}, status=400)
        try:
            bus_trip = BusTrip.objects.get(id=bus_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Bus trip does not exist'}, status=404)
        serializer = BusTripSerializer(bus_trip)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'status': 'false', 'message': 'Only POST and GET'}, status=405)


def get_random_bus_trip(request):
    """
    Returns random bus trip
    Params:
        None
    Status:
        404: There are no bus trips
        405: Wrong method
    Returns: BusTrip
        {
            id, origin: {id, name, state, city, address}, destination: {id,
            name, state, city, address}, departure_date, arrival_date
        }
    """
    if request.method == 'GET':
        if len(BusTrip.objects.all()) == 0:
            return JsonResponse({'status': 'false', 'message': 'There are no bus trips'}, status=404)
        bus_trip_id = randint(1, len(BusTrip.objects.all()))
        bus_trip = BusTrip.objects.get(id=bus_trip_id)
        serializer = BusTripSerializer(bus_trip)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)
