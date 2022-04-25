from random import randint
from aircraft_type import AircraftType
from abc import abstractmethod


class Airport:
    def __init__(self, aircraft_type: AircraftType):
        self.aircraft_type = aircraft_type
        self.icao = None
        self.departure_procedure = None
        self.climb = None
        self.initial = None
        self.dep_freq = None
        self.digit1 = None
        self.digit2 = None
        self.digit3 = None
        self.digit4 = None
        self.all_gates = None

    def get_squawk(self):
        """Return a random squawk code based on the ranges outlined in the specific airport's .py file"""
        digit1 = self.digit1
        digit2 = randint(self.digit2[0], self.digit2[1])
        digit3 = randint(self.digit3[0], self.digit3[1])
        digit4 = randint(self.digit4[0], self.digit4[1])
        return str(digit1) + str(digit2) + str(digit3) + str(digit4)  # Each digit must be separate because only digits 0-7 can be used in squawk codes, not 8 or 9

    @abstractmethod
    def get_initial(self):
        pass

    @abstractmethod
    def get_climb(self, route):
        pass
