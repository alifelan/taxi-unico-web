from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('user/', views.user, name='user'),
    path('user/<str:email>', views.user_details, name='user_details'),
    path('taxi/<int:id>', views.taxi_details, name='taxi_details'),
    path('userTaxiTrips/<str:email>', views.get_user_taxi_trips, name='user_taxi_trips'),
    path('createTaxiTrip/', views.create_taxi_trip, name='create_taxi_trip'),
    path('busTrip/', views.post_bus_trip, name='post_bus_trip'),
    path('busTrip/<int:id>', views.get_bus_trip, name='get_bus_trip'),
    path('randomBusTrip/', views.get_random_bus_trip, name='get_random_bus_trip'),
    path('login/', views.login, name='login'),
    path('startTrip/', views.start_trip, name='start_trip'),
    path('rateDriver/', views.rate_driver, name='rate_driver'),
    path('rateUser/', views.rate_user, name='rate_user'),
    path('getCurrentOrNext/<str:email>', views.get_current_or_next_trip, name='get_current_or_next_trip'),
]
