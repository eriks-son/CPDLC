import ops
from airports import ewr, jfk, phl, lga

AIRPORT_LIST = ["KEWR", "KJFK", "KLGA", "KPHL"]


class Airport:
    def __init__(self, category: str, route: str):
        self.route = route
        self.category = category
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

    def specific_airport(self):
        if self.icao == "KEWR":
            self.initial = ewr.get_initial(self.dep_runway)
            self.departure_procedure = "EWR4"
            self.climb = "NEWARK FOUR (EWR4)"
        if self.icao == "KJFK":
            self.departure_procedure, self.climb = jfk.get_climb(self.dep_runway, self.category, self.route)
            self.initial = jfk.get_initial(self.climb)
        if self.icao == "KPHL":
            self.initial = phl.get_initial(self.category)
            self.departure_procedure = "PHL2"
            self.climb = "PHILADELPHIA TWO (PHL2)"
        if self.icao == "LGA":
            self.departure_procedure, self.climb = lga.get_climb(self.dep_runway, self.category, self.route, self.arr_runway)
            self.initial = lga.get_initial(self.departure_procedure, self.climb)
