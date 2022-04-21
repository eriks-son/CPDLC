import requests
from string import ascii_letters as LETTERS, digits as DIGITS
from altitude import Altitude
from airport import Airport
from aircraft_type import AircraftType

IGNORE = -100  # Ignore all routes with this (easier than popping from the dict since dicts are not hashable inside dicts)


# noinspection PyTypeChecker
class Route:
    """Reads route from the flight plan and checks the PRD database to see if changes must be made"""

    def __init__(self, departure: Airport, arrival: str):
        """Initializes the requested route and adds any FAA PRD routes to the list"""
        self.route = None
        self.departure = departure
        self.arrival = arrival
        self.attempt = requests.get(f'https://5n1v87j7va.execute-api.us-east-1.amazonaws.com/Prod/route?from={departure.icao[1:]}&to={arrival[1:]}').json()
        self.prd = []
        self.options = []
        for route in self.attempt['body']['routes']:
            if not route['pref']:
                self.prd.append(route)
                self.options.append(0)

    def __str__(self):
        """Returns just the route. If the route is user-inputted, just return the string, otherwise return the route index of the PRD route"""
        if type(self.route) is str:  # If the PRD isn't chosen
            return self.route
        return self.route['route']  # Otherwise, there is a PRD route

    def get_route(self):
        """
        Get the user inputted route, then check if a valid exit gate is in the route
        """
        while True:
            route = input("Please enter your entire route: ")
            gates = self.departure.get_exit_gates()
            for gate in gates:
                if gate in route:
                    self.route = route
            if route is not None:
                break
            print("No valid departure gate in the route. Please include at least one of the following exit gates in the beginning of the route: ")
            for gate in gates:
                print(gate, end=" ")
            print()

    def check_altitude_col(self, altitude: Altitude, aircraft_type: AircraftType):
        """Checks the altitude column for both altitude and aircraft type
        altitude: requested altitude
        category: aircraft category ("JET" or "PROP")
        opposite: opposite category of category
        All parameters will come from the flight_plan object and will be passed as arguments
        """

        for index, route in enumerate(self.prd):
            # Checks if it is a ZNY route and to make sure it's a string
            if self.options[index] <= IGNORE:  # Skip all ignored routes
                continue

            if route['alt'] == '':
                continue

            # Checks for aircraft type
            if aircraft_type.category in route['alt']:
                self.options[index] += 2
            if aircraft_type.opposite in route['alt']:
                self.options[index] = IGNORE
                continue

            # Checks altitude
            if '0' not in route['alt']:  # Makes sure there is an altitude value
                continue

            if '-' in route['alt']:  # Check if it is an altitude range
                route_altitude = ''.join(char for char in route['alt'] if char not in LETTERS).strip()
                min_altitude, max_altitude = tuple(route_altitude.split('-'))
                if int(min_altitude) <= int(altitude) <= int(max_altitude):
                    self.options[index] += 1

            elif '<' in route['alt'] or "MAX" in route['alt'] or "BELOW" in route['alt'] or "AOB" in route['alt']:  # Checks if there is a max altitude
                route_altitude = ''.join(char for char in route['alt'] if char in DIGITS)
                if int(altitude) <= int(route_altitude):
                    self.options[index] += 1
                else:
                    self.options[index] -= 1

            elif '>' in route['alt'] or "MIN" in route['alt'] or "ABOVE" in route['alt'] or "AOA" in route['alt']:  # Checks if there is a min altitude
                route_altitude = ''.join(char for char in route['alt'] if char in DIGITS)
                if int(altitude) >= int(route_altitude):
                    self.options[index] += 1
                else:
                    self.options[index] -= 1

            else:  # Catches exact altitudes
                route_altitude = ''.join(char for char in route['alt'] if char in DIGITS)
                if int(altitude) <= int(route_altitude)/100:
                    self.options[index] += 2
                else:
                    self.options[index] -= 1

    def check_specific_col(self, col: str, aircraft_type: AircraftType):
        """Checks the specified column for aircraft type
        col: the key for the column of the prd. Used for both area and aircraft columns
        aircraft_type: used for both the category, opposite and turbo parameters
        """
        for index, route in enumerate(self.prd):
            if self.options[index] <= IGNORE:  # Skip all ignored routes
                continue

            if route[col] == '':
                continue

            # Checks for aircraft type and turbo (if applicable)
            if aircraft_type.category == "JET" and aircraft_type.category in route[col]:
                self.options[index] += 2
            if aircraft_type.category == "PROP" and aircraft_type.category in route[col]:
                if "210" in route[col]:
                    if ">" in route[col] or "GREATER" in route[col]:
                        if aircraft_type.turbo:
                            self.options[index] += 3
                        else:
                            self.options[index] = IGNORE
                            continue
                    if "<" in route[col] or "LESS" in route[col]:
                        if not aircraft_type.turbo:
                            self.options[index] += 3
                        else:
                            self.options[index] = IGNORE
                            continue
                else:
                    self.options[index] += 2

            # Checks if the opposite aircraft type is in the column
            if aircraft_type.opposite in route[col]:
                self.options[index] = IGNORE

    def get_prd_route(self, altitude: Altitude, aircraft_type: AircraftType):
        """Uses the above functions to find the best PRD route. Then it replaces the user's route with the PRD route"""
        self.check_altitude_col(altitude, aircraft_type)
        self.check_specific_col('area', aircraft_type)
        self.check_specific_col('aircraft', aircraft_type)
        if len(self.prd):  # If there is a valid PRD route to be assigned
            self.route = self.prd[self.options.index(max(self.options))]

    def check_altitude(self, altitude: Altitude):
        """Checks if the PRD route has a mandatory altitude"""
        if type(self.route) is str:  # If the route is user inputted, there is no altitude requirement
            return altitude.alt

        if '0' not in self.route['alt']:  # Makes sure there is an altitude value
            return altitude.alt

        if '-' in self.route['alt']:  # Check if it is an altitude range
            route_altitude = ''.join(char for char in self.route['alt'] if char not in LETTERS).strip()
            min_altitude, max_altitude = tuple(route_altitude.split('-'))
            if int(altitude) > int(max_altitude):
                return max_altitude
            elif int(altitude) < int(min_altitude):
                return min_altitude
            else:
                return altitude.alt

        elif '<' in self.route['alt'] or "MAX" in self.route['alt'] or "BELOW" in self.route['alt'] or "AOB" in self.route['alt']:  # Checks if there is a max altitude
            route_altitude = ''.join(char for char in self.route['alt'] if char in DIGITS)
            if int(altitude) > int(route_altitude):
                if len(route_altitude) > 3:
                    return '0' + route_altitude[:2]
                return route_altitude
            else:
                return altitude.alt

        elif '>' in self.route['alt'] or "MIN" in self.route['alt'] or "ABOVE" in self.route['alt'] or "AOA" in self.route['alt']:  # Checks if there is a min altitude
            route_altitude = ''.join(char for char in self.route['alt'] if char in DIGITS)
            if int(altitude) < int(route_altitude):
                if len(route_altitude) > 3:
                    return '0' + route_altitude[:2]
                return route_altitude
            else:
                return altitude.alt

        else:  # Catches exact altitudes
            route_altitude = ''.join(char for char in self.route['alt'] if char in DIGITS)
            if len(route_altitude) > 3:
                return '0' + route_altitude[:2]
            return route_altitude

    def check_dep_proc(self, departure: Airport):
        """Adds the departure airport's departure procedure to the beginning of the route"""
        for gate in departure.get_exit_gates():
            if gate in str(self):  # This will always trigger at least once because the route must already have an exit gate
                disregard, exit_gate, rest = str(self).partition(gate)
                break
        route = f"{departure.departure_procedure} {exit_gate}{rest}"
        if type(self.route) is str:  # If it's user inputted
            self.route = route
        else:  # If it's a preferred route
            self.route['route'] = route
