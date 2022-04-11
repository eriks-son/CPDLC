import numpy
import math
import pickle


class Airport:
    def __init__(self, icao: str, latitude: float, longitude: float, name: str):
        self.icao = icao
        self.latitude = latitude
        self.longitude = longitude
        self.name = name

    def __str__(self):
        print(f'ICAO: {self.icao} ({name})\tLatitude: {self.latitude}\tLongitude: {self.longitude}')


class AirportDatabase:
    def __init__(self):
        self.database = {}

    def add_airport(self, icao: str, latitude: float, longitude: float, name: str):
        self.database[icao] = Airport(icao, latitude, longitude, name)

    def get_lat_and_long(self, icao: str):
        return self.database[icao].latitude, self.database[icao].longitude

    def get_airport_name(self, icao: str):
        return self.database[icao].name

    def is_in_list(self, icao: str):
        if icao in self.database:
            return True
        return False

    def get_track(self, departure: str, arrival: str):
        lat1, lat2, lon1, lon2 = self.database[departure].latitude, self.database[arrival].latitude, self.database[departure].longitude, self.database[arrival].longitude
        delta_lon = lon2 - lon1
        x = math.cos(math.radians(lat2)) * math.sin(math.radians(delta_lon))
        y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(delta_lon))
        track = numpy.arctan2(x, y)
        return numpy.degrees(track)


with open('airport_database.dat', 'rb') as f:
    database = pickle.load(f)
print(database.get_airport_name("KPTW"))
