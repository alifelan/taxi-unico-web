# taxi-unico-web

## Descripción

Backend web del proyecto semestral de la clase "Proyecto de desarrollo de aplicaciones móviles"

## https://taxi-unico-api.herokuapp.com/user/
    user works with POST and PUT,

    POST:
        Receives a json with data te create a user.
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



## https://taxi-unico-api.herokuapp.com/createTaxiTrip/
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
            id, origin: {id, name, state, city, address}, destination: {id,
            name, state, city, address}, departure_date, arrival_date
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
            id, origin: {id, name, state, city, address}, destination: {id,
            name, state, city, address}, departure_date, arrival_date
        }



## https://taxi-unico-api.herokuapp.com/login/
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


## https://taxi-unico-api.herokuapp.com/taxi/<id>
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
            id, origin: {id, name, state, city, address}, destination: {id,
            name, state, city, address}, date, bus_trip: {id, origin: {id, name,
            state, city, address}, destination: {id, name, state, city,
            address}, departure_date, arrival_date}, user: {name, email},
            taxi: {id, driver_name, plate, model, brand, taxi_number}, price,
            taxi_rating, user_rating
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
            id, origin: {id, name, state, city, address}, destination: {id,
            name, state, city, address}, date, bus_trip: {id, origin: {id, name,
            state, city, address}, destination: {id, name, state, city,
            address}, departure_date, arrival_date}, user: {name, email},
            taxi: {id, driver_name, plate, model, brand, taxi_number}, price,
            taxi_rating, user_rating
        }
