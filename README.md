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
                name, email
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
                name, email
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
            taxi: {id, driver_name, plate, model, brand, taxi_number}
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
            taxi: {id, driver_name, plate, model, brand, taxi_number, price}
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
