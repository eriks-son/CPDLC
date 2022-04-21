import ops
from random import randint
from aircraft_type import AircraftType
from airports import ewr, jfk, phl, lga

AIRPORT_LIST = ["KEWR", "KJFK", "KLGA", "KPHL"]


class Airport:
    def __init__(self):
        self.route = None
        self.icao = None
        self.departure_procedure = None
        self.climb = None
        self.initial = None
        self.get_icao()
        self.dep_runway, self.arr_runway = ops.get_ops(self.icao)

    def get_icao(self):
        while True:
            self.icao = input("Please enter the ICAO of your departure airport: ")
            if self.icao not in AIRPORT_LIST:
                print(f"{self.icao} is not a supported airport. Here are the currently supported departure airports:")
                for airport in AIRPORT_LIST:
                    print(airport)
            else:
                break

    def insert_route(self, route):
        self.route = route

    def specific_airport(self, route, aircraft_type: AircraftType):
        if self.icao == "KEWR":
            self.initial = ewr.get_initial(self.dep_runway)
            self.departure_procedure = "EWR4"
            if "WHITE" in str(route) or "DIXIE" in str(route):
                self.departure_procedure = self.departure_procedure + " ELVAE COL"
            if aircraft_type.category == "PROP":
                for gate in ewr.EAST:
                    if gate in str(route):
                        self.departure_procedure = self.departure_procedure + " BREZY V39 CMK"
            self.climb = "NEWARK FOUR (EWR4)"
        if self.icao == "KJFK":
            self.departure_procedure, self.climb = jfk.get_climb(self.dep_runway, aircraft_type.category, str(route))
            self.initial = jfk.get_initial(self.climb)
        if self.icao == "KPHL":
            self.initial = phl.get_initial(aircraft_type.category)
            self.departure_procedure = "PHL2"
            self.climb = "PHILADELPHIA TWO (PHL2)"
        if self.icao == "KLGA":
            self.departure_procedure, self.climb = lga.get_climb(self.dep_runway, aircraft_type.category, str(route), self.arr_runway)
            self.initial = lga.get_initial(self.departure_procedure, self.climb)

    def get_squawk(self):
        if self.icao == "KEWR":
            digit1 = ewr.DIGIT1
            digit2 = randint(ewr.DIGIT2[0], ewr.DIGIT2[1])
            digit3 = randint(ewr.DIGIT3[0], ewr.DIGIT3[1])
            digit4 = randint(ewr.DIGIT4[0], ewr.DIGIT4[1])
        if self.icao == "KJFK":
            digit1 = jfk.DIGIT1
            digit2 = randint(jfk.DIGIT2[0], jfk.DIGIT2[1])
            digit3 = randint(jfk.DIGIT3[0], jfk.DIGIT3[1])
            digit4 = randint(jfk.DIGIT4[0], jfk.DIGIT4[1])
        if self.icao == "KLGA":
            digit1 = lga.DIGIT1
            digit2 = randint(lga.DIGIT2[0], lga.DIGIT2[1])
            digit3 = randint(lga.DIGIT3[0], lga.DIGIT3[1])
            digit4 = randint(lga.DIGIT4[0], lga.DIGIT4[1])
        if self.icao == "KPHL":
            digit1 = phl.DIGIT1
            digit2 = randint(phl.DIGIT2[0], phl.DIGIT2[1])
            digit3 = randint(lga.DIGIT3[0], lga.DIGIT3[1])
            digit4 = randint(lga.DIGIT4[0], lga.DIGIT4[1])
        return str(digit1) + str(digit2) + str(digit3) + str(digit4)

    def get_dep_freq(self):
        if self.icao == "KEWR":
            return ewr.DEP_FREQ
        if self.icao == "KJFK":
            return jfk.DEP_FREQ
        if self.icao == "KLGA":
            return lga.DEP_FREQ
        if self.icao == "KPHL":
            return phl.DEP_FREQ

    def get_exit_gates(self):
        if self.icao == "KEWR":
            return ewr.ALL
        if self.icao == "KJFK":
            return jfk.ALL
        if self.icao == "KLGA":
            return lga.ALL
        if self.icao == "KPHL":
            return phl.ALL
