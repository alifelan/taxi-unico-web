from taxi.models import User, State, City, Taxi, TaxiTrip, BusTrip, Location
from datetime import datetime

ali = User(name="Ali Felan", email="alifelanv@gmail.com", password="123", card="1234123412341234")
ali.save()
pepe = User(name="Jose Cruz", email="jcfflores@gmail.com", password="123", card="1234123412341234")
pepe.save()
raul = User(name="Raul Herrera", email="raulhs@gmail.com", password="123", card="1234123412341234")
raul.save()
pablo = User(name="Pablo Andrade", email="paundra@gmail.com",
             password="123", card="1234123412341234")
pablo.save()

coah = State(state="Coahuila")
coah.save()
nl = State(state="Nuevo Leon")
nl.save()

mva = City(city="Monclova", state=coah)
mva.save()
mty = City(city="Monterrey", state=nl)
mty.save()
sal = City(city="Saltillo", state=coah)
sal.save()

tec = Location(name="Tecnologico de Monterrey", city=mty,
               address="Av. Eugenio Garza Sada 2501 Sur", latitude=25.651299, longitude=-100.289856)
tec.save()
depas = Location(name="Departamentos de todos", city=mty, address="Fisicos 118",
                 latitude=25.651937, longitude=-100.293450)
depas.save()
bus_mty = Location(name="Central de autobuses Monterrey", city=mty,
                   address="Avenida Cristóbal Colón 855", latitude=25.687118, longitude=-100.319857)
bus_mty.save()
casa = Location(name="Casa de Ali en Monclova", city=mva, address="Privada Felan",
                latitude=26.917940, longitude=-101.424006)
casa.save()
bus_mva = Location(name="Central de autobuses Monclova", city=mva,
                   address="Zona centro", latitude=26.902346, longitude=-101.419034)
bus_mva.save()
fundidora = Location(name="Parque fundidora", city=mty,
                     address="Av. Parque Fundidora 501", latitude=25.678863, longitude=-100.284231)
fundidora.save()
bus_sal = Location(name="Central de autobuses Saltillo", city=sal,
                   address="Periférico Luis Echeverría 999", latitude=25.397814, longitude=-101.007726)
bus_sal.save()
museo = Location(name="Museo del Desierto", city=sal,
                 address="Blvd. Carlos Abedrop Dávila 3745", latitude=25.413736, longitude=-100.964321)
museo.save()


ulises = Taxi(driver_name="Ulises", email="ulises@gmail.com", password="123",
              plate="ABC1234", model="Model 3", brand="Tesla", taxi_number=1, city=mty)
ulises.save()
neto = Taxi(driver_name="Ernesto", email="neto@gmail.com", password="123",
            plate="ABC1235", model="Model 3", brand="Tesla", taxi_number=2, city=mty)
neto.save()
osko = Taxi(driver_name="Oscar", email="oscar@gmail.com", password="123",
            plate="ABC1236", model="Model 3", brand="Tesla", taxi_number=3, city=mty)
osko.save()
juan = Taxi(driver_name="Juan", email="juan@gmail.com", password="123",
            plate="ABC1237", model="Model 3", brand="Tesla", taxi_number=4, city=mva)
juan.save()
luis = Taxi(driver_name="Luis", email="luis@gmail.com", password="123",
            plate="ABC1238", model="Model 3", brand="Tesla", taxi_number=5, city=mva)
luis.save()


uno = datetime.strptime('5/7/19 12:00', '%m/%d/%y %H:%M')
dos = datetime.strptime('5/7/19 15:00', '%m/%d/%y %H:%M')
tres = datetime.strptime('5/14/19 11:00', '%m/%d/%y %H:%M')
cuatro = datetime.strptime('5/14/19 14:00', '%m/%d/%y %H:%M')
cinco = datetime.strptime('5/16/19 16:00', '%m/%d/%y %H:%M')
seis = datetime.strptime('5/16/19 19:00', '%m/%d/%y %H:%M')
siete = datetime.strptime('5/9/19 15:00', '%m/%d/%y %H:%M')
ocho = datetime.strptime('5/9/19 17:00', '%m/%d/%y %H:%M')
nueve = datetime.strptime('5/10/19 12:00', '%m/%d/%y %H:%M')
diez = datetime.strptime('5/10/19 14:00', '%m/%d/%y %H:%M')
once = datetime.strptime('5/9/19 13:00', '%m/%d/%y %H:%M')
doce = datetime.strptime('5/9/19 16:00', '%m/%d/%y %H:%M')
trece = datetime.strptime('5/9/19 14:00', '%m/%d/%y %H:%M')
catorce = datetime.strptime('5/9/19 17:00', '%m/%d/%y %H:%M')


mva_mty = BusTrip(origin=bus_mva, destination=bus_mty,
                  first_departure_date=uno, first_arrival_date=dos)
mva_mty.save()
mva_mty_round = BusTrip(origin=bus_mva, destination=bus_mty, first_departure_date=tres,
                        first_arrival_date=cuatro, second_departure_date=cinco, second_arrival_date=seis, round_trip=True)
mva_mty_round.save()
mva_sal = BusTrip(origin=bus_mva, destination=bus_sal, first_departure_date=siete,
                  first_arrival_date=ocho, second_departure_date=nueve, second_arrival_date=diez, round_trip=True)
mva_sal.save()
mva_mty2 = BusTrip(origin=bus_mva, destination=bus_mty,
                   first_departure_date=once, first_arrival_date=doce)
mva_mty2.save()
mty_mva = BusTrip(origin=bus_mty, destination=bus_mva,
                  first_departure_date=trece, first_arrival_date=catorce)
mva_mty.save()


uno = datetime.strptime('5/7/19 11:00', '%m/%d/%y %H:%M')
uno2 = datetime.strptime('5/7/19 11:30', '%m/%d/%y %H:%M')
dos = datetime.strptime('5/7/19 15:10', '%m/%d/%y %H:%M')
dos2 = datetime.strptime('5/7/19 15:40', '%m/%d/%y %H:%M')
tres = datetime.strptime('5/14/19 11:00', '%m/%d/%y %H:%M')
cuatro = datetime.strptime('5/14/19 14:00', '%m/%d/%y %H:%M')
cinco = datetime.strptime('5/16/19 16:00', '%m/%d/%y %H:%M')
seis = datetime.strptime('5/16/19 19:00', '%m/%d/%y %H:%M')
siete = datetime.strptime('5/9/19 14:00', '%m/%d/%y %H:%M')
siete2 = datetime.strptime('5/9/19 14:30', '%m/%d/%y %H:%M')
ocho = datetime.strptime('5/9/19 17:00', '%m/%d/%y %H:%M')
ocho2 = datetime.strptime('5/9/19 17:30', '%m/%d/%y %H:%M')
nueve = datetime.strptime('5/10/19 12:00', '%m/%d/%y %H:%M')
nueve2 = datetime.strptime('5/10/19 11:00', '%m/%d/%y %H:%M')
nueve3 = datetime.strptime('5/10/19 11:30', '%m/%d/%y %H:%M')
diez = datetime.strptime('5/10/19 14:00', '%m/%d/%y %H:%M')
diez2 = datetime.strptime('5/10/19 14:30', '%m/%d/%y %H:%M')
once = datetime.strptime('5/9/19 13:00', '%m/%d/%y %H:%M')
doce = datetime.strptime('5/9/19 16:00', '%m/%d/%y %H:%M')
trece = datetime.strptime('5/9/19 14:00', '%m/%d/%y %H:%M')
catorce = datetime.strptime('5/9/19 17:00', '%m/%d/%y %H:%M')
catorce2 = datetime.strptime('5/9/19 17:30', '%m/%d/%y %H:%M')


TaxiTrip(origin=casa, destination=bus_mva, departure_date=uno, arrival_date=uno2, bus_trip=mva_mty, user=ali, taxi=luis, price=75.50, taxi_rating=4,
         user_rating=5, distance_meters=1024, distance_string="1024 metros", time_seconds=1024, time_string="1024 segundos", status='PA').save()
TaxiTrip(origin=bus_mty, destination=tec, departure_date=dos, arrival_date=dos2, bus_trip=mva_mty, user=ali, taxi=ulises, price=72.50, taxi_rating=5,
         user_rating=2, distance_meters=1025, distance_string="1025 metros", time_seconds=1025, time_string="1025 segundos", status='PA').save()
TaxiTrip(origin=bus_mva, destination=casa, departure_date=once, arrival_date=doce, bus_trip=mva_mty_round, user=ali, taxi=juan,
         price=85.50, distance_meters=1026, distance_string="1026 metros", time_seconds=1026, time_string="1026 segundos", status='CA').save()
TaxiTrip(origin=bus_mva, destination=casa, departure_date=once, arrival_date=doce, bus_trip=mva_mty_round, user=ali, taxi=luis, price=70.50,
         taxi_rating=5, user_rating=5, distance_meters=1026, distance_string="1026 metros", time_seconds=1026, time_string="1026 segundos", status='PE').save()
TaxiTrip(origin=tec, destination=bus_mty, departure_date=nueve, arrival_date=diez, bus_trip=mva_mty_round, user=ali, taxi=neto, price=700.50,
         taxi_rating=5, user_rating=5, distance_meters=1026, distance_string="1026 metros", time_seconds=1026, time_string="1026 segundos", status='PE').save()
TaxiTrip(origin=bus_mva, destination=bus_sal, departure_date=siete, arrival_date=siete2, bus_trip=mva_sal, user=ali, taxi=luis, price=16.07,
         user_rating=5, distance_meters=1027, distance_string="1027 metros", time_seconds=1027, time_string="1027 segundos", status='PA').save()
TaxiTrip(origin=bus_sal, destination=museo, departure_date=ocho, arrival_date=ocho2, bus_trip=mva_sal, user=ali, taxi=juan, price=16.07,
         taxi_rating=5, user_rating=2, distance_meters=1027, distance_string="1027 metros", time_seconds=1027, time_string="1027 segundos").save()
TaxiTrip(origin=museo, destination=bus_sal, departure_date=nueve2, arrival_date=nueve3, bus_trip=mva_sal, user=ali, taxi=juan, price=16.07,
         taxi_rating=3, user_rating=3, distance_meters=1027, distance_string="1027 metros", time_seconds=1027, time_string="1027 segundos").save()
TaxiTrip(origin=bus_mva, destination=casa, departure_date=diez, arrival_date=diez2, bus_trip=mva_sal, user=ali, taxi=luis, price=20.07,
         taxi_rating=4, user_rating=4, distance_meters=1027, distance_string="1027 metros", time_seconds=1027, time_string="1027 segundos").save()
TaxiTrip(origin=bus_mty, destination=fundidora, departure_date=catorce, arrival_date=catorce2, bus_trip=mva_mty2, user=ali, taxi=ulises, price=20.07,
         taxi_rating=4, user_rating=4, distance_meters=1027, distance_string="1027 metros", time_seconds=1027, time_string="1027 segundos").save()
