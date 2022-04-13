import requests
from string import ascii_letters as LETTERS, digits as DIGITS


class Route:
    """Reads route from the flight plan and checks the PRD database to see if changes must be made"""

    def __init__(self, rt: str, departure: str, arrival: str):
        """Initializes the requested route and adds any FAA PRD routes to the list"""
        self.route = rt
        self.prd_route = None
        self.attempt = requests.get(f'https://5n1v87j7va.execute-api.us-east-1.amazonaws.com/Prod/route?from={departure[1:]}&to={arrival[1:]}').json()
        self.prd = []
        self.options = []
        for route in self.attempt['body']['routes']:
            if not route['pref']:
                self.prd.append(route)
                self.options.append(0)

    def __str__(self):
        """Returns just the route (the rest is only for PRD purposes)"""
        return self.route

    def check_altitude_col(self, altitude: int, category: str, opposite: str):
        """Checks the altitude column for both altitude and aircraft type
        altitude: requested altitude
        category: aircraft category ("JET" or "PROP")
        opposite: opposite category of category
        All parameters will come from the flight_plan object and will be passed as arguments
        """

        for index, route in enumerate(self.prd):
            # Checks if it is a ZNY route and to make sure it's a string
            if route['alt'] != '':
                continue

            # Checks for aircraft type
            if category in route['alt']:
                self.options[index] += 2
            if opposite in route['alt']:
                self.prd.remove(route)
                self.options.pop(index)
                continue

            # Checks altitude
            if '0' not in route['alt']:  # Makes sure there is an altitude value
                continue

            if '-' in route['alt']:  # Check if it is an altitude range
                route_altitude = ''.join(char for char in route['alt'] if char not in LETTERS).strip()
                min_altitude, max_altitude = tuple(route_altitude.split('-'))
                if int(min_altitude) <= altitude <= int(max_altitude):
                    self.options[index] += 1

            elif '<' in route['alt'] or "MAX" in route['alt'] or "BELOW" in route['alt']:  # Checks if there is a max altitude
                route_altitude = ''.join(char for char in route['alt'] if char in DIGITS)
                if altitude <= int(route_altitude):
                    self.options[index] += 1
                else:
                    self.options[index] -= 1

            elif '>' in route['alt'] or "MIN" in route['alt'] or "ABOVE" in route['alt']:  # Checks if there is a min altitude
                route_altitude = ''.join(char for char in route['alt'] if char in DIGITS)
                if altitude >= int(route_altitude):
                    self.options[index] += 1
                else:
                    self.options[index] -= 1

            else:  # Catches exact altitudes
                route_altitude = ''.join(char for char in route['alt'] if char in DIGITS)
                if altitude <= int(route_altitude)/100:
                    self.options[index] += 2
                else:
                    self.options[index] -= 1

    def check_specific_col(self, col: str, category: str, opposite: str, turbo: bool):
        """Checks the specified column for aircraft type
        col: the key for the column of the prd. Used for both area and aircraft columns
        category: aircraft category ("JET" or "PROP")
        opposite: opposite category of category
        turbo: True if the aircraft is a turboprop, False if else
        """
        for index, route in enumerate(self.prd):
            # Checks if it is a ZNY route and to make sure it's a string
            if route[col] == '':
                continue

            # Checks for aircraft type and turbo (if applicable)
            if category == "JET" and category in route[col]:
                self.options[index] += 2
            if category == "PROP" and category in route[col]:
                if "210" in route[col]:
                    if ">" in route[col] or "GREATER" in route[col]:
                        if turbo:
                            self.options[index] += 3
                        else:
                            self.prd.remove(route)
                            self.options.pop(index)
                            continue
                    if "<" in route[col] or "LESS" in route[col]:
                        if not turbo:
                            self.options[index] += 3
                        else:
                            self.prd.remove(route)
                            self.options.pop(index)
                            continue
                else:
                    self.options[index] += 2

            # Checks if the opposite aircraft type is in the column
            if opposite in route[col]:
                self.prd.remove(route)
                self.options.pop(index)

    def get_prd_route(self, altitude: int, col: str, category: str, opposite: str, turbo: bool):
        self.check_altitude_col(altitude, category, opposite)
        self.check_specific_col('area', category, opposite, turbo)
        self.check_specific_col('aircraft', category, opposite, turbo)
        self.prd_route = self.prd[self.options.index(max(self.options))]
        self.route = self.prd_route['route']
