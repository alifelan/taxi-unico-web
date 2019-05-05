from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from taxi.models import Taxi, User, Location, BusTrip, TaxiTrip, State, City
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
                name, email, rating, trips
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
        card = user.card
        for key in body.keys():
            if key == 'name':
                name = body[key]
            elif key == 'password':
                password = body[key]
            elif key == 'card':
                card = body[key]
        user = User(name=name, email=user_email, password=password, card=card)
        user.save()
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only POST and PUT'}, status=405)


@csrf_exempt
def user_details(request, email):
    """
    Returns details of a user
    Param:
        email: user email
    Status:
        400: Missing data in json
        404: User does not exist
        405: Wrong method
    Returns: User
        {
            name, email, rating, trips
        }
    """
    if request.method == 'GET':
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


@csrf_exempt
def taxi_details(request, id):
    """
    Returns details of a taxi
    Param:
        id: taxi id
    Status:
        400: Missing data in json
        404: Taxi does not exist
        405: Wrong method
    Returns: Taxi
        {
            id, driver_name, plate, model, brand, taxi_number, city, rating, trips
        }
    """
    if request.method == 'GET':
        try:
            taxi = Taxi.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Taxi does not exist'}, status=404)
        serializer = TaxiSerializer(taxi)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


@csrf_exempt
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
    if request.method == 'POST':
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
    return JsonResponse({'status': 'false', 'message': 'Only POST'}, status=405)


def get_user_taxi_trips(request, email):
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
            taxi: {id, driver_name, plate, model, brand, taxi_number}, price,
            taxi_rating, user_rating
        }]
    """
    if request.method == 'GET':
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        user_taxi_trips = user.taxiTrips.all()
        serializer = TaxiTripSerializer(user_taxi_trips, many=True)
        response = {"data": serializer.data}
        return JsonResponse(response, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


@csrf_exempt
def rate_driver(request):
    """
    Adds rating to driver in taxi trip
    Param:
        taxiTripId: Id of the taxi trip
        rating: Rating given to the driver in a scale of 1 to 5
    Status:
        400: Missing data in json
        404: Taxi trip does not exist
        405: Wrong method
        412: Rating is not an integer between 1 and 5
    Returns: TaxiTrip
        {
            id, origin: {id, name, state, city, address}, destination: {id,
            name, state, city, address}, date, bus_trip: {id, origin: {id, name,
            state, city, address}, destination: {id, name, state, city,
            address}, departure_date, arrival_date}, user: {name, email},
            taxi: {id, driver_name, plate, model, brand, taxi_number}, price,
            taxi_rating, user_rating
        }
    """
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        try:
            taxi_trip_id = body['taxiTripId']
            rating = body['rating']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        if int(rating) < 1 or int(rating) > 5:
            return JsonResponse({'status': 'false', 'message': 'Rating not in range 1-5'}, status=412)
        try:
            taxi_trip = TaxiTrip.objects.get(id=taxi_trip_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Taxi trip does not exist'}, status=404)
        taxi_trip.taxi_rating = rating
        taxi_trip.save()
        serializer = TaxiTripSerializer(taxi_trip)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only POST'}, status=405)


@csrf_exempt
def rate_user(request):
    """
    Adds rating to user in taxi trip
    Param:
        taxiTripId: Id of the taxi trip
        rating: Rating given to the user in a scale of 1 to 5
    Status:
        400: Missing data in json
        404: Taxi trip does not exist
        405: Wrong method
        412: Rating is not an integer between 1 and 5
    Returns: TaxiTrip
        {
            id, origin: {id, name, state, city, address}, destination: {id,
            name, state, city, address}, date, bus_trip: {id, origin: {id, name,
            state, city, address}, destination: {id, name, state, city,
            address}, departure_date, arrival_date}, user: {name, email},
            taxi: {id, driver_name, plate, model, brand, taxi_number}, price,
            taxi_rating, user_rating
        }
    """
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        try:
            taxi_trip_id = body['taxiTripId']
            rating = body['rating']
            arrival_date = body['arrivalDate']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        if int(rating) < 1 or int(rating) > 5:
            return JsonResponse({'status': 'false', 'message': 'Rating not in range 1-5'}, status=412)
        try:
            taxi_trip = TaxiTrip.objects.get(id=taxi_trip_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Taxi trip does not exist'}, status=404)
        taxi_trip.user_rating = rating
        taxi_trip.arrival_date = datetime.strptime(arrival_date, '%m/%d/%y %H:%M')
        taxi_trip.save()
        serializer = TaxiTripSerializer(taxi_trip)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only POST'}, status=405)


@csrf_exempt
def create_taxi_trip(request):
    """
    Creates a taxi trip with data received. If it receives origin, it puts
    bus trip destination as destination, and viceversa
    Param:
        origin (optional): Origin data
            name: Name
            state: State
            city: City
            address: Address
        destionation (optional): Destination data
            name: Name
            state: State
            city: City
            address: Address
        date: Date and time of the trip, in format Month/Day/Year Hour:Minutes
        busTripId: Identifier of the bus trip
        userEmail (optional): user email
        price: trip price
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
            taxi: {id, driver_name, plate, model, brand, taxi_number}, price,
            taxi_rating, user_rating
        }
    """
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        try:
            price = body['price']
            date = datetime.now()
            if 'date' in body:
                date = datetime.strptime(body['date'], '%m/%d/%y %H:%M')
            bus_trip_id = body['busTripId']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        try:
            user_email = body['email']
            try:
                user = User.objects.get(email=user_email)
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        except KeyError:
            user = None
        try:
            bus_trip = BusTrip.objects.get(id=bus_trip_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Bus trip does not exist'}, status=404)
        try:
            origin_json = body['origin']
            name = origin_json['name']
            state = origin_json['state']
            city = origin_json['city']
            address = origin_json['address']
            try:
                origin_state = State.objects.get(state=state)
            except ObjectDoesNotExist:
                origin_state = State(state=state)
                origin_state.save()
            try:
                origin_city = City.objects.get(state=origin_state, city=city)
            except ObjectDoesNotExist:
                origin_city = City(state=origin_state, city=city)
                origin_city.save()
            try:
                origin = Location.objects.get(
                    city=origin_city, name=name, address=address)
            except ObjectDoesNotExist:
                origin = Location(city=origin_city, address=address, name=name)
                origin.save()
            destination = bus_trip.destination
        except KeyError:
            try:
                destination_json = body['destination']
                name = destination_json['name']
                state = destination_json['state']
                city = destination_json['city']
                address = destination_json['address']
            except KeyError:
                return JsonResponse({'status': 'false', 'message': 'Bus trip does not exist'}, status=404)
            try:
                destination_state = State.objects.get(state=state)
            except ObjectDoesNotExist:
                destination_state = State(state=state)
                destination_state.save()
            try:
                destination_city = City.objects.get(state=destination_state, city=city)
            except ObjectDoesNotExist:
                destination_city = City(state=destination_state, city=city)
                destination_city.save()
            try:
                destination = Location.objects.get(
                    city=destination_city, name=name, address=address)
            except ObjectDoesNotExist:
                destination = Location(city=destination_city, address=address, name=name)
                destination.save()
            origin = bus_trip.destination
        trips = TaxiTrip.objects.filter(arrival_date=date)
        busy_local_taxis = {trip.taxi for trip in trips if trip.taxi.city == origin.city}
        free_taxis = set(Taxi.objects.all()) - busy_local_taxis
        if len(free_taxis) > 0:
            taxi = list(free_taxis)[0]
        else:
            return JsonResponse({'status': 'false', 'message': 'All taxis are busy at that time'}, status=403)
        taxi_trip = TaxiTrip(origin=origin, destination=destination, departure_date=date, arrival_date=None,
                             bus_trip=bus_trip, user=user, taxi=taxi, price=price)
        taxi_trip.save()
        serializer = TaxiTripSerializer(taxi_trip)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only POST'}, status=405)


def get_bus_trip(request, id):
    """
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
    if request.method == 'GET':
        try:
            bus_trip = BusTrip.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Bus trip does not exist'}, status=404)
        serializer = BusTripSerializer(bus_trip)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


@csrf_exempt
def post_bus_trip(request):
    """
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
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode("utf-8"))
            origin_json = body['origin']
            o_name = origin_json['name']
            o_state = origin_json['state']
            o_city = origin_json['city']
            o_address = origin_json['address']
            destination_json = body['destination']
            d_name = destination_json['name']
            d_state = destination_json['state']
            d_city = destination_json['city']
            d_address = destination_json['address']
            date = datetime.now()
            if 'date' in body:
                date = datetime.strptime(body['date'], '%m/%d/%y %H:%M')
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        try:
            origin_state = State.objects.get(state=o_state)
        except ObjectDoesNotExist:
            origin_state = State(state=o_state)
            origin_state.save()
        try:
            origin_city = City.objects.get(state=origin_state, city=o_city)
        except ObjectDoesNotExist:
            origin_city = City(state=origin_state, city=o_city)
            origin_city.save()
        try:
            origin = Location.objects.get(
                city=origin_city, name=o_name, address=o_address)
        except ObjectDoesNotExist:
            origin = Location(city=origin_city, address=o_address, name=o_name)
            origin.save()
        try:
            destination_state = State.objects.get(state=d_state)
        except ObjectDoesNotExist:
            destination_state = State(state=d_state)
            destination_state.save()
        try:
            destination_city = City.objects.get(state=destination_state, city=d_city)
        except ObjectDoesNotExist:
            destination_city = City(state=destination_state, city=d_city)
            destination_city.save()
        try:
            destination = Location.objects.get(
                city=destination_city, name=d_name, address=d_address)
        except ObjectDoesNotExist:
            destination = Location(city=destination_city, address=d_address, name=d_name)
            destination.save()
        bus_trip = BusTrip(origin=origin, destination=destination,
                           departure_date=date, arrival_date=date)
        bus_trip.save()
        serializer = BusTripSerializer(bus_trip)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'status': 'false', 'message': 'Only POST'}, status=405)


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
