# taxi-unico-web

## Descripción

Backend web del proyecto semestral de la clase "Proyecto de desarrollo de aplicaciones móviles"

Meaning of status:
-CA: CANCELLED
-PE: PENDING
-AC: ACTIVE
-PA: PAST

## https://taxi-unico-api.herokuapp.com/user/
    user works with POST and PUT,

    POST:
        Receives a json with data to create a user.
        Param:
            name: User name
            email: User email
            password: User password
            card: Credit card
        Status:
            400: Missing data in json
            405: User exists, use PUT to update data
        Returns: User
            {
                name, email, rating, trips
            }

    PUT:
        Updates user with data received in json
        Param:
            email: User email
            name (optional): New name
            password (optional): New password
        Status:
            400: Missing data in json
            404: User does not exist
        Returns: User
            {
                name, email, rating, trips
            }



## https://taxi-unico-api.herokuapp.com/userTaxiTrips/<email>
    Returns taxi trips of a user
    Param:
        None
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


## https://taxi-unico-api.herokuapp.com/taxiTaxiTrips/<email>
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



## https://taxi-unico-api.herokuapp.com/createTaxiTrip/
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
            address, latitude, longitude}, departure_date, arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        }



## https://taxi-unico-api.herokuapp.com/busTrip/
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


## https://taxi-unico-api.herokuapp.com/busTrip/<id>
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



## https://taxi-unico-api.herokuapp.com/randomBusTrip/
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



## https://taxi-unico-api.herokuapp.com/userLogin/
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


## https://taxi-unico-api.herokuapp.com/taxiLogin/
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


## https://taxi-unico-api.herokuapp.com/user/<email>
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


## https://taxi-unico-api.herokuapp.com/taxi/<email>
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


## https://taxi-unico-api.herokuapp.com/rateDriver
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


## https://taxi-unico-api.herokuapp.com/rateUser
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


## https://taxi-unico-api.herokuapp.com/getCurrentOrNext/<email>
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
        }}


## https://taxi-unico-api.herokuapp.com/getTaxiCurrentOrNext/<email>
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


## https://taxi-unico-api.herokuapp.com/startTrip/
    Start taxi trip
    Param:
        taxiTripId: Id of the taxi trip|
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


## https://taxi-unico-api.herokuapp.com/cancelTrip/
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


## https://taxi-unico-api.herokuapp.com/getUserBusTrips/<int:bus_trip_id>/<str:email>
    Returns user's trips on a bus trip
    Param:
        bus_trip_id: bus trip id
        email: user email
    Status:
        404: User or bus trip does not exist
        405: Wrong method
    Returns: [TaxiTrip]
        {trips: [
            id, origin: {id, name, state, city, address, latitude, longitude},
            destination: {id, name, state, city, address, latitude, longitude},
            date, bus_trip: {id, origin: {id, name, state, city, address,
            latitude, longitude}, destination: {id, name, state, city,
            address, latitude, longitude}, first_departure_date, first_arrival_date,
            second_departure_date, second_arrival_date, round_trip},
            user: {name, email}, taxi: {driver_name, email, plate, model, brand,
            taxi_number}, price, taxi_rating, user_rating, status
        ]}


## https://taxi-unico-api.herokuapp.com/updateTaxiTripLocation/
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
        change: 1 to change origin, 2 to change destination
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
