from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from taxi.models import Taxi, User, Location, BusTrip, TaxiTrip, State, City
from taxi.serializers import TaxiSerializer, UserSerializer, LocationSerializer, BusTripSerializer, TaxiTripSerializer
from datetime import datetime, timedelta
from django.utils import timezone
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
def taxi_details(request, email):
    """
    Returns details of a taxi
    Param:
        email: taxi email
    Status:
        400: Missing data in json
        404: Taxi does not exist
        405: Wrong method
    Returns: Taxi
        {
            email, driver_name, plate, model, brand, taxi_number, city, rating, trips
        }
    """
    if request.method == 'GET':
        try:
            taxi = Taxi.objects.get(email=email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Taxi does not exist'}, status=404)
        serializer = TaxiSerializer(taxi)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


@csrf_exempt
def user_login(request):
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


@csrf_exempt
def taxi_login(request):
    """
    Login checks email and password received
    Param:
        email: Taxi email
        password: Taxi password
    Status:
        400: Missing data in json
        404: Taxi email does not exist
        200: Success
        403: Wrong password
        405: Wrong method
    Returns:
        {status, message}
    """
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        try:
            taxi_email = body['email']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        try:
            taxi = Taxi.objects.get(email=taxi_email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        taxi_password = body['password']
        if taxi.password == taxi_password:
            return JsonResponse({'status': 'true', 'message': 'Success on loging in'}, status=200)
        return JsonResponse({'status': 'false', 'message': 'Wrong password'}, status=403)
    return JsonResponse({'status': 'false', 'message': 'Only POST'}, status=405)


@csrf_exempt
def get_user_taxi_trips(request, email):
    """
    Returns taxi trips of a user
    Param:
        email: user email
    Status:
        404: User does not exist
        405: Wrong method
    Returns: [TaxiTrip]
        {past_trips: [{
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }], future_trips: [{
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }], current_trip: [{
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }], cancelled_trips: [{
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }]}
    """
    if request.method == 'GET':
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        current_trip = user.taxiTrips.filter(status='AC')
        past_trips = user.taxiTrips.filter(status='PA')
        future_trips = user.taxiTrips.filter(status='PE')
        cancelled_trips = user.taxiTrips.filter(status='CA')
        current_serializer = TaxiTripSerializer(current_trip, many=True)
        past_serializer = TaxiTripSerializer(past_trips, many=True)
        future_serializer = TaxiTripSerializer(future_trips, many=True)
        cancelled_serializer = TaxiTripSerializer(cancelled_trips, many=True)
        response = {'past_trips': past_serializer.data,
                    'future_trips': future_serializer.data, 'current_trip': current_serializer.data, 'cancelled_trips': cancelled_serializer.data}
        return JsonResponse(response, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


@csrf_exempt
def get_taxi_taxi_trips(request, email):
    """
    Returns taxi trips of a taxi
    Param:
        email: taxi email
    Status:
        404: Taxi does not exist
        405: Wrong method
    Returns: [TaxiTrip]
        {past_trips: [{
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }], future_trips: [{
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }], current_trip: [{
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }], cancelled_trips: [{
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }]}
    """
    if request.method == 'GET':
        try:
            taxi = Taxi.objects.get(email=email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        current_trip = taxi.trips.filter(status='AC')
        past_trips = taxi.trips.filter(status='PA')
        future_trips = taxi.trips.filter(status='PE')
        cancelled_trips = taxi.trips.filter(status='CA')
        current_serializer = TaxiTripSerializer(current_trip, many=True)
        past_serializer = TaxiTripSerializer(past_trips, many=True)
        future_serializer = TaxiTripSerializer(future_trips, many=True)
        cancelled_serializer = TaxiTripSerializer(cancelled_trips, many=True)
        response = {'past_trips': past_serializer.data,
                    'future_trips': future_serializer.data, 'current_trip': current_serializer.data, 'cancelled_trips': cancelled_serializer.data}
        return JsonResponse(response, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


@csrf_exempt
def get_bus_email_trips(request, bus_trip_id, email):
    """
    Returns user's trips on a bus trip
    Param:
        bus_trip_id: bus trip id
        email: user email
    Status:
        404: User or bus trip does not exist
        405: Wrong method
    Returns: [TaxiTrip]
        {trip1: [
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        ], trip2: [
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        ], trip3: [
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        ], trip4: [
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        ]}
    """
    if request.method == 'GET':
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        try:
            bus_trip = BusTrip.objects.get(id=bus_trip_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Bus trip does not exist'}, status=404)
        taxi_trips = bus_trip.taxiTrips.filter(user=user).exclude(status='CA')
        trip1 = taxi_trips.filter(destination=bus_trip.origin)
        trip2 = taxi_trips.filter(origin=bus_trip.destination)
        trip3 = taxi_trips.filter(destination=bus_trip.destination)
        trip4 = taxi_trips.filter(origin=bus_trip.origin)
        serializer1 = TaxiTripSerializer(trip1, many=True)
        serializer2 = TaxiTripSerializer(trip2, many=True)
        serializer3 = TaxiTripSerializer(trip3, many=True)
        serializer4 = TaxiTripSerializer(trip4, many=True)
        response = {'trip1': serializer1.data, 'trip2': serializer2.data,
                    'trip3': serializer3.data, 'trip4': serializer4.data}
        return JsonResponse(response, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


@csrf_exempt
def get_user_current_or_next_trip(request, email):
    """
    Returns current or next taxi trip
    Param:
        email: user email
    Status:
        404: User does not exist
        405: Wrong method
    Returns: [TaxiTrip]
        {current, taxi_trip: {
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }, rate: {
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }
    """
    if request.method == 'GET':
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'User does not exist'}, status=404)
        current_trip = user.taxiTrips.filter(status='AC')
        current = True
        if len(current_trip) == 0:
            current = False
            trips = user.taxiTrips.filter(status='PE').order_by('departure_date')
            if len(trips) == 0:
                return JsonResponse({'current': current, 'taxi_trip': ''}, safe=False)
            else:
                taxi_trip = trips[0]
        else:
            taxi_trip = current_trip[0]
        rate_trips = user.taxiTrips.filter(status='PA').filter(taxi_rating=None)
        if len(rate_trips) > 0:
            rate_trips = rate_trips[0:1]
        serializer = TaxiTripSerializer(taxi_trip)
        rate_serializer = TaxiTripSerializer(rate_trips, many=True)
        response = {'current': current, 'taxi_trip': serializer.data, 'rate': rate_serializer.data}
        return JsonResponse(response, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


@csrf_exempt
def get_taxi_current_or_next_trip(request, email):
    """
    Returns current or next taxi trip
    Param:
        email: taxi email
    Status:
        404: Taxi does not exist
        405: Wrong method
    Returns: [TaxiTrip]
        {current, taxi_trip: {
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }}
    """
    if request.method == 'GET':
        try:
            taxi = Taxi.objects.get(email=email)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Taxi does not exist'}, status=404)
        current_trip = taxi.trips.filter(status='AC')
        current = True
        if len(current_trip) == 0:
            current = False
            trips = taxi.trips.filter(status='PE').order_by('departure_date')
            if len(trips) == 0:
                return JsonResponse({'current': current, 'taxi_trip': ''}, safe=False)
            else:
                taxi_trip = trips[0]
        else:
            taxi_trip = current_trip[0]
        serializer = TaxiTripSerializer(taxi_trip)
        response = {'current': current, 'taxi_trip': serializer.data}
        return JsonResponse(response, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only GET'}, status=405)


@csrf_exempt
def start_trip(request):
    """
    Start taxi trip
    Param:
        taxiTripId: Id of the taxi trip
    Status:
        400: Missing data in json
        404: Taxi trip does not exist
        405: Wrong method
        412: Rating is not an integer between 1 and 5
    Returns: TaxiTrip
        {
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }
    """
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        try:
            taxi_trip_id = body['taxiTripId']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        try:
            taxi_trip = TaxiTrip.objects.get(id=taxi_trip_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Taxi trip does not exist'}, status=404)
        taxi_trip.departure_date = timezone.now()
        taxi_trip.status = 'AC'
        taxi_trip.save()
        serializer = TaxiTripSerializer(taxi_trip)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only POST'}, status=405)


@csrf_exempt
def cancel_trip(request):
    """
    Cancel taxi trip
    Param:
        taxiTripId: Id of the taxi trip
    Status:
        400: Missing data in json
        404: Taxi trip does not exist
        405: Wrong method
    Returns: TaxiTrip
        {
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }
    """
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        try:
            taxi_trip_id = body['taxiTripId']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        try:
            taxi_trip = TaxiTrip.objects.get(id=taxi_trip_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Taxi trip does not exist'}, status=404)
        taxi_trip.status = 'CA'
        taxi_trip.save()
        serializer = TaxiTripSerializer(taxi_trip)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only POST'}, status=405)


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
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }
    """
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        try:
            taxi_trip_id = body['taxiTripId']
            rating = body['rating']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        if float(rating) < 1 or float(rating) > 5:
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
    Adds rating to user in taxi trip and saves arrival date.
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
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
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
        taxi_trip.user_rating = rating
        taxi_trip.arrival_date = timezone.now()
        taxi_trip.status = 'PA'
        taxi_trip.save()
        serializer = TaxiTripSerializer(taxi_trip)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only POST'}, status=405)


@csrf_exempt
def update_taxi_trip_location(request):
    """
    Updates location of taxi trip.
    Param:
        taxiTripId: Taxi trip id
        location:
            name: Name
            state: State
            city: City
            address: Address
            latitude: Latitude
            longitude: Longitude
    Status:
        400: Missing data in json
        404: Taxi trip does not exist
        405: Wrong method
        412: Change is not 1 or 2
    Returns: TaxiTrip
        {
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }
    """
    if request.method == 'PUT':
        body = json.loads(request.body.decode("utf-8"))
        try:
            taxi_trip_id = body['taxiTripId']
            change = body['change']
            location_json = body['location']
            location_name = location_json['name']
            location_state = location_json['state']
            location_city = location_json['city']
            location_address = location_json['address']
            location_latitude = location_json['latitude']
            location_longitude = location_json['longitude']
            try:
                state = State.objects.get(state=location_state)
            except ObjectDoesNotExist:
                state = State(state=location_state)
                state.save()
            try:
                city = City.objects.get(state=state, city=location_city)
            except ObjectDoesNotExist:
                city = City(state=state, city=location_city)
                city.save()
            try:
                location = Location.objects.get(
                    city=city, name=location_name, address=location_address,)
            except ObjectDoesNotExist:
                location = Location(city=city, address=location_address, name=location_name,
                                    latitude=location_latitude, longitude=location_longitude)
                location.save()
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        try:
            taxi_trip = TaxiTrip.objects.get(id=taxi_trip_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'false', 'message': 'Taxi trip does not exist'}, status=404)
        if taxi_trip.destination == taxi_trip.bus_trip.origin:
            taxi_trip.origin = location
        elif taxi_trip.origin == taxi_trip.bus_trip.destination:
            taxi_trip.destination = location
        elif taxi_trip.destination == taxi_trip.bus_trip.destination:
            taxi_trip.origin = location
        elif taxi_trip.origin == taxi_trip.bus_trip.origin:
            taxi_trip.destination = location
        taxi_trip.save()
        serializer = TaxiTripSerializer(taxi_trip)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({'status': 'false', 'message': 'Only PUT'}, status=405)


@csrf_exempt
def create_taxi_trip(request):
    """
    Creates a taxi trip with data received. It receives a number to identify
    the trip, so it can know from where to where its going.
    Param:
        Location:
            name: Name
            state: State
            city: City
            address: Address
            latitude: Latitude
            longitude: Longitude
        busTripId: Identifier of the bus trip
        trip: Number from 1 to 4, symbolizing if its a trip from origin to origin
            station with 1, a trip from destination station to destination with 2,
            from destination to destination station with 3 or from origin station
            to origin with 4.
        userEmail (optional): user email
        price: trip price
        duration:
            value: Value in seconds
            text: Value as string
        distance:
            value: Value in meters
            text: Value as string
    Status:
        400: Missing data in json
        404: User or bus trip does not exist
        403: All taxis are busy
        405: Wrong method
        412: Trip is not between 1 and 4 or bus trip is not a round trip
    Returns: TaxiTrip
        {
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }
    """
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        try:
            price = body['price']
            bus_trip_id = body['busTripId']
            distance_json = body['distance']
            distance_meters = distance_json['value']
            distance_string = distance_json['text']
            time_json = body['duration']
            time_seconds = time_json['value']
            time_string = time_json['text']
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
            location_json = body['location']
            location_name = location_json['name']
            location_state = location_json['state']
            location_city = location_json['city']
            location_address = location_json['address']
            location_latitude = location_json['latitude']
            location_longitude = location_json['longitude']
            try:
                state = State.objects.get(state=location_state)
            except ObjectDoesNotExist:
                state = State(state=location_state)
                state.save()
            try:
                city = City.objects.get(state=state, city=location_city)
            except ObjectDoesNotExist:
                city = City(state=state, city=location_city)
                city.save()
            try:
                location = Location.objects.get(
                    city=city, name=location_name, address=location_address,)
            except ObjectDoesNotExist:
                location = Location(city=city, address=location_address, name=location_name,
                                    latitude=location_latitude, longitude=location_longitude)
                location.save()
            trip = body['trip']
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Missing data'}, status=400)
        if int(trip) == 1:
            arrival_date = bus_trip.first_departure_date - timedelta(minutes=30)
            departure_date = arrival_date - timedelta(seconds=int(time_seconds))
            trips = TaxiTrip.objects.filter(arrival_date__gte=departure_date).filter(
                departure_date__lte=arrival_date)
            busy_local_taxis = {trip.taxi for trip in trips if trip.taxi.city == location.city}
            free_taxis = set(Taxi.objects.all()) - busy_local_taxis
            if len(free_taxis) > 0:
                taxi = list(free_taxis)[0]
            else:
                return JsonResponse({'status': 'false', 'message': 'All taxis are busy at that time'}, status=403)
            taxi_trip = TaxiTrip(origin=location, destination=bus_trip.origin, departure_date=departure_date, arrival_date=arrival_date,
                                 bus_trip=bus_trip, user=user, taxi=taxi, price=price, distance_meters=distance_meters,
                                 distance_string=distance_string, time_seconds=time_seconds, time_string=time_string)
        elif int(trip) == 2:
            departure_date = bus_trip.first_arrival_date
            arrival_date = departure_date + timedelta(seconds=int(time_seconds))
            trips = TaxiTrip.objects.filter(arrival_date__gte=departure_date).filter(
                departure_date__lte=arrival_date)
            busy_local_taxis = {trip.taxi for trip in trips if trip.taxi.city == location.city}
            free_taxis = set(Taxi.objects.all()) - busy_local_taxis
            if len(free_taxis) > 0:
                taxi = list(free_taxis)[0]
            else:
                return JsonResponse({'status': 'false', 'message': 'All taxis are busy at that time'}, status=403)
            taxi_trip = TaxiTrip(origin=bus_trip.destination, destination=location, departure_date=departure_date, arrival_date=arrival_date,
                                 bus_trip=bus_trip, user=user, taxi=taxi, price=price, distance_meters=distance_meters,
                                 distance_string=distance_string, time_seconds=time_seconds, time_string=time_string)
        elif int(trip) == 3 and bus_trip.round_trip:
            arrival_date = bus_trip.second_departure_date - timedelta(minutes=30)
            departure_date = arrival_date - timedelta(seconds=int(time_seconds))
            trips = TaxiTrip.objects.filter(arrival_date__gte=departure_date).filter(
                departure_date__lte=arrival_date)
            busy_local_taxis = {trip.taxi for trip in trips if trip.taxi.city == location.city}
            free_taxis = set(Taxi.objects.all()) - busy_local_taxis
            if len(free_taxis) > 0:
                taxi = list(free_taxis)[0]
            else:
                return JsonResponse({'status': 'false', 'message': 'All taxis are busy at that time'}, status=403)
            taxi_trip = TaxiTrip(origin=location, destination=bus_trip.destination, departure_date=departure_date, arrival_date=arrival_date,
                                 bus_trip=bus_trip, user=user, taxi=taxi, price=price, distance_meters=distance_meters,
                                 distance_string=distance_string, time_seconds=time_seconds, time_string=time_string)
        elif int(trip) == 4 and bus_trip.round_trip:
            departure_date = bus_trip.second_arrival_date
            arrival_date = departure_date + timedelta(seconds=int(time_seconds))
            trips = TaxiTrip.objects.filter(arrival_date__gte=departure_date).filter(
                departure_date__lte=arrival_date)
            busy_local_taxis = {trip.taxi for trip in trips if trip.taxi.city == location.city}
            free_taxis = set(Taxi.objects.all()) - busy_local_taxis
            if len(free_taxis) > 0:
                taxi = list(free_taxis)[0]
            else:
                return JsonResponse({'status': 'false', 'message': 'All taxis are busy at that time'}, status=403)
            taxi_trip = TaxiTrip(origin=bus_trip.destination, destination=location, departure_date=departure_date, arrival_date=arrival_date,
                                 bus_trip=bus_trip, user=user, taxi=taxi, price=price, distance_meters=distance_meters,
                                 distance_string=distance_string, time_seconds=time_seconds, time_string=time_string)
        else:
            return JsonResponse({'status': 'false', 'message': 'Trip is not a number between 1 and 4 or bus trip is not a round trip'}, status=412)
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
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip
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
        roundTrip (optional): True if its a round trip
    Status:
        400: Missing data in json
        404: User or bus trip does not exist
        403: All taxis are busy
        405: Wrong method
    Returns: BusTrip
        {
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip
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
            try:
                round_trip = body['roundTrip']
            except KeyError:
                round_trip = False
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
                           first_departure_date=date, first_arrival_date=date,
                           second_departure_date=None, second_arrival_date=None,
                           round_trip=round_trip)
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
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip
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
