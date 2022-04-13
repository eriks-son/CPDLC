import requests
import ewr
import jfk
AIRPORT_LIST = ["KEWR", "KJFK", "KLGA", "KPHL"]


class Airport:
    def __init__(self, category: str, route: str):
        self.route = route
        self.category = category
        self.icao = None
        self.departure_procedure = None
        self.climb = None
        self.initial = None
        self.dep_runway = ""
        self.arr_runway = ""
        self.get_icao()
        self.get_ops()

    def get_icao(self):
        while True:
            self.icao = input("Please enter the ICAO of your departure airport: ")
            if self.icao not in AIRPORT_LIST:
                print(f"{self.icao} is not a supported airport. Here are the currently supported departure airports:")
                for airport in AIRPORT_LIST:
                    print(airport)
            else:
                break

    def get_ops(self):
        attempt = requests.get(f'https://datis.clowd.io/api/{self.icao}')
        atis = attempt.json()[0]['datis']
        # 14: is used so that ARR/DEP at the beginning of some ATISes are not caught
        before, middle, after = atis[14:].partition("DEP")
        found_digit = False
        for x in range(len(before) - 1, 0, -1):
            if before[x].isdigit():
                found_digit = True
                self.arr_runway = before[x] + self.arr_runway
            elif found_digit:
                break

        found_digit = False
        for x in after:
            if x.isdigit():
                found_digit = True
                self.dep_runway += x
            elif found_digit:
                break

    def specific_airport(self):
        if self.icao == "KEWR":
            self.initial = ewr.get_initial(self.dep_runway)
            self.departure_procedure = "EWR4"
            self.climb = "NEWARK FOUR (EWR4)"
        if self.icao == "KJFK":
            self.departure_procedure, self.climb = jfk.get_climb(self.dep_runway, self.category, self.route)
            self.initial = jfk.get_initial(self.climb)
