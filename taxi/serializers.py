from rest_framework import serializers
from taxi.models import Taxi, User, TaxiTrip, BusTrip, Location


class TaxiSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Taxi
        fields = ('id', 'driver_name', 'plate', 'model', 'brand', 'taxi_number', 'city')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email')


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
        fields = ('id', 'origin', 'destination', 'departure_date', 'arrival_date')


class TaxiTripSerializer(serializers.ModelSerializer):
    origin = LocationSerializer(read_only=True)
    destination = LocationSerializer(read_only=True)
    bus_trip = BusTripSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    taxi = TaxiSerializer(read_only=True)

    class Meta:
        model = TaxiTrip
        fields = ('id', 'origin', 'destination', 'departure_date',
                  'arrival_date', 'bus_trip', 'user', 'taxi', 'price')
