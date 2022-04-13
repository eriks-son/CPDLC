from string import ascii_letters as LETTERS, digits as DIGITS


class FlightPlan:
    """FlightPlan class for storing an aircraft's filed flight plan"""

    def __init__(self, callsign: str, departure: str, arrival: str, aircraft_type: str, route: str, altitude: int):
        """Initialize a Flight Plan"""
        self.category = None  # JET or PROP
        self.opposite = None  # Opposite of above
        self.turbo = None  # If an aircraft is above/below 210 kts (True is above)
        self.callsign = callsign
        self.departure = departure
        self.arrival = arrival
        self.aircraft_type = aircraft_type
        self.route = route
        self.altitude = altitude

    def __str__(self):
        """Print out each part of the flight plan on a line"""
        return f"Callsign: {self.callsign}\nDeparture Airport: {self.departure}\nArrival Airport: {self.arrival}\nAircraft Type: {self.aircraft_type}\nCruise Altitude: {self.altitude}"

    def get_aircraft_category(self):
        if self.aircraft_type in JETS:
            self.category = "JET"
            self.opposite = "PROP"
        elif self.aircraft_type in PROPS:
            self.category = "PROP"
            self.opposite = "JET"
            self.turbo = False
        elif self.aircraft_type in TURBOPROPS:
            self.category = "PROP"
            self.opposite = "JET"
            self.turbo = True

    def check_if_faa(self):
        for index, value in enumerate(self.table["ZNY Pref"]):
            if type(value) is str:
                self.options[index] = ZNYPRD

    def check_specific_col(self, col):
        """Checks the specified column for aircraft type"""
        for index, value in enumerate(self.table[col]):
            # Checks if it is a ZNY route and to make sure it's a string
            if self.options[index] == ZNYPRD or type(value) is not str:
                continue

            # Checks for aircraft type and turbo (if applicable)
            if self.category == "JET" and self.category in value:
                self.options[index] += 2
            if self.category == "PROP" and self.category in value:
                if "210" in value:
                    if ">" in value or "GREATER" in value:
                        if self.turbo:
                            self.options[index] += 3
                        else:
                            self.options[index] -= 3
                    if "<" in value or "LESS" in value:
                        if not self.turbo:
                            self.options[index] += 3
                        else:
                            self.options[index] -= 3
                else:
                    self.options[index] += 2
            if self.opposite in value:
                self.options[index] = ZNYPRD

    def check_altitude_col(self):
        """Checks the altitude column for both altitude and aircraft type"""
        for index, value in enumerate(self.table["Altitude"]):
            # Checks if it is a ZNY route and to make sure it's a string
            if self.options[index] == ZNYPRD or type(value) is not str:
                continue

            # Checks for aircraft type
            if self.category in value:
                self.options[index] += 2
            if self.opposite in value:
                self.options[index] = ZNYPRD

            # Checks altitude
            if '0' not in value:  # Makes sure there is an altitude value
                continue

            if '-' in value:  # Check if it is an altitude range
                altitude = ''.join(char for char in value if char not in LETTERS).strip()
                min_altitude, max_altitude = tuple(altitude.split('-'))
                if int(min_altitude) <= self.altitude <= int(max_altitude):
                    self.options[index] += 1
                else:
                    self.options[index] -= 1

            elif '<' in value or "MAX" in value or "BELOW" in value:  # Checks if there is a max altitude
                altitude = ''.join(char for char in value if char in DIGITS)
                if self.altitude <= int(altitude):
                    self.options[index] += 1
                else:
                    self.options[index] -= 1

            elif '>' in value or "MIN" in value or "ABOVE" in value:  # Checks if there is a min altitude
                altitude = ''.join(char for char in value if char in DIGITS)
                if self.altitude >= int(altitude):
                    self.options[index] += 1
                else:
                    self.options[index] -= 1

            else:  # Catches exact altitudes
                altitude = ''.join(char for char in value if char in DIGITS)
                if self.altitude <= int(altitude)/100:
                    self.options[index] += 2
                else:
                    self.options[index] -= 1

    def choose_prd_route(self):
        self.route = self.table["Route"][self.options.index(max(self.options))]


sample = FlightPlan("AAL1", "KEWR", "KBDL", "DH8A", "BDR", 90)
sample.get_aircraft_category()
sample.check_if_faa()
for column in ["Area", "Aircraft"]:
    sample.check_specific_col(column)
sample.check_altitude_col()
sample.choose_prd_route()
print(sample.route)
