from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('user/', views.user, name='user'),
    path('userTaxiTrips/', views.get_user_taxi_trips, name='user_taxi_trips'),
    path('createTaxiTrip/', views.create_taxi_trip, name='create_taxi_trip'),
    path('busTrip/', views.bus_trip, name='bus_trip'),
    path('randomBusTrip/', views.get_random_bus_trip, name='get_random_bus_trip'),
]
