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

ulises = Taxi(driver_name="Ulises", email="ulises@gmail.com", password="123",
              plate="ABC1234", model="No se", brand="Tmpc se", taxi_number=1, city=mty)
ulises.save()
neto = Taxi(driver_name="Ernesto", email="neto@gmail.com", password="123",
            plate="ABC1234", model="No se", brand="Tmpc se", taxi_number=2, city=mty)
neto.save()
osko = Taxi(driver_name="Oscar", email="oscar@gmail.com", password="123",
            plate="ABC1234", model="No se", brand="Tmpc se", taxi_number=3, city=mty)
osko.save()
juan = Taxi(driver_name="Juan", email="juan@gmail.com", password="123",
            plate="ABC1234", model="No se", brand="Tmpc se", taxi_number=4, city=mva)
juan.save()
luis = Taxi(driver_name="Luis", email="luis@gmail.com", password="123",
            plate="ABC1234", model="No se", brand="Tmpc se", taxi_number=5, city=mva)
luis.save()

uno = datetime.strptime('5/7/19 12:00', '%m/%d/%y %H:%M')
dos = datetime.strptime('5/7/19 15:00', '%m/%d/%y %H:%M')
tres = datetime.strptime('5/14/19 11:00', '%m/%d/%y %H:%M')
cuatro = datetime.strptime('5/14/19 14:00', '%m/%d/%y %H:%M')
cinco = datetime.strptime('5/16/19 16:00', '%m/%d/%y %H:%M')
seis = datetime.strptime('5/16/19 19:00', '%m/%d/%y %H:%M')

mva_mty = BusTrip(origin=bus_mva, destination=bus_mty,
                  first_departure_date=uno, first_arrival_date=dos)
mva_mty.save()
mva_mty_round = BusTrip(origin=bus_mva, destination=bus_mty, first_departure_date=tres,
                        first_arrival_date=cuatro, second_departure_date=cinco, second_arrival_date=seis, round_trip=True)
mva_mty_round.save()

siete = datetime.strptime('5/7/19 11:00', '%m/%d/%y %H:%M')
ocho = datetime.strptime('5/7/19 11:30', '%m/%d/%y %H:%M')
nueve = datetime.strptime('5/7/19 15:00', '%m/%d/%y %H:%M')
diez = datetime.strptime('5/7/19 15:30', '%m/%d/%y %H:%M')
once = datetime.strptime('5/16/19 19:00', '%m/%d/%y %H:%M')
doce = datetime.strptime('5/16/19 19:30', '%m/%d/%y %H:%M')

TaxiTrip(origin=casa, destination=bus_mva, departure_date=siete, arrival_date=ocho, bus_trip=mva_mty, user=ali, taxi=luis, price=75.50, taxi_rating=4,
         user_rating=5, distance_meters=1024, distance_string="1024 metros", time_seconds=1024, time_string="1024 segundos", status='PA').save()
TaxiTrip(origin=bus_mty, destination=tec, departure_date=nueve, arrival_date=diez, bus_trip=mva_mty, user=ali, taxi=ulises, price=72.50, taxi_rating=5,
         user_rating=2, distance_meters=1025, distance_string="1025 metros", time_seconds=1025, time_string="1025 segundos", status='AC').save()
TaxiTrip(origin=bus_mva, destination=casa, departure_date=once, arrival_date=doce, bus_trip=mva_mty_round, user=ali, taxi=juan,
         price=85.50, distance_meters=1026, distance_string="1026 metros", time_seconds=1026, time_string="1026 segundos", status='CA').save()
TaxiTrip(origin=bus_mva, destination=casa, departure_date=once, arrival_date=doce, bus_trip=mva_mty_round, user=ali, taxi=luis, price=70.50,
         taxi_rating=5, user_rating=5, distance_meters=1026, distance_string="1026 metros", time_seconds=1026, time_string="1026 segundos", status='PE').save()
TaxiTrip(origin=tec, destination=bus_mty, departure_date=nueve, arrival_date=diez, bus_trip=mva_mty_round, user=ali, taxi=neto, price=700.50,
         taxi_rating=5, user_rating=5, distance_meters=1026, distance_string="1026 metros", time_seconds=1026, time_string="1026 segundos", status='PE').save()
