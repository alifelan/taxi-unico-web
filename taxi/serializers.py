from rest_framework import serializers
from taxi.models import Taxi, User, TaxiTrip, BusTrip, Location


class TaxiSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    rating = serializers.SerializerMethodField()
    trips = serializers.SerializerMethodField()

    class Meta:
        model = Taxi
        fields = ('id', 'driver_name', 'plate', 'model', 'brand',
                  'taxi_number', 'city', 'rating', 'trips')

    def get_rating(self, obj):
        number_of_trips = len(TaxiTrip.objects.filter(taxi=obj).exclude(taxi_rating=None))
        if number_of_trips == 0:
            return 5
        return sum(trip.taxi_rating for trip in TaxiTrip.objects.filter(taxi=obj).exclude(taxi_rating=None)) / len(TaxiTrip.objects.filter(taxi=obj).exclude(taxi_rating=None))

    def get_trips(self, obj):
        return len(TaxiTrip.objects.filter(taxi=obj).exclude(taxi_rating=None))


class UserSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    trips = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('name', 'email', 'rating', 'trips')

    def get_rating(self, obj):
        number_of_trips = len(TaxiTrip.objects.filter(user=obj).exclude(user_rating=None))
        if number_of_trips == 0:
            return 5
        return sum(trip.user_rating for trip in TaxiTrip.objects.filter(user=obj).exclude(user_rating=None)) / len(TaxiTrip.objects.filter(user=obj).exclude(user_rating=None))

    def get_trips(self, obj):
        return len(TaxiTrip.objects.filter(user=obj).exclude(user_rating=None))


class LocationSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = ('id', 'name', 'city', 'address')


class BusTripSerializer(serializers.ModelSerializer):
    origin = LocationSerializer(read_only=True)
    destination = LocationSerializer(read_only=True)

    class Meta:
        model = BusTrip
        fields = ('id', 'origin', 'destination', 'departure_date', 'arrival_date', 'round_trip')


class TaxiTripSerializer(serializers.ModelSerializer):
    origin = LocationSerializer(read_only=True)
    destination = LocationSerializer(read_only=True)
    bus_trip = BusTripSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    taxi = TaxiSerializer(read_only=True)

    class Meta:
        model = TaxiTrip
        fields = ('id', 'origin', 'destination', 'departure_date',
                  'arrival_date', 'bus_trip', 'user', 'taxi', 'price',
                  'taxi_rating', 'user_rating')
