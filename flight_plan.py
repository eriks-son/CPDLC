from aircraft_type import AircraftType
from altitude import Altitude
from route import Route
from airport import Airport
from datetime import datetime, timezone


class FlightPlan:
    """FlightPlan class for storing an aircraft's filed flight plan"""

    def __init__(self, callsign: str, departure: Airport, arrival: str, aircraft_type: AircraftType, route: Route,
                 altitude: Altitude):
        """Initialize a Flight Plan"""
        self.callsign = callsign
        self.departure = departure
        self.arrival = arrival
        self.aircraft_type = aircraft_type
        self.route = route
        self.altitude = altitude

    def __str__(self):
        """Print out each part of the flight plan on a line"""
        return f"Callsign: {self.callsign}\nDeparture Airport: {self.departure}\nArrival Airport: {self.arrival}\nAircraft Type: {self.aircraft_type}\nCruise Altitude: {self.altitude}"

    def get_clearance(self):
        print(
            f"""\nPRE-DEPARTURE CLEARANCE START | {datetime.now(timezone.utc)} Z | CALLSIGN: {self.callsign} | AIRCRAFT: {self.aircraft_type}\nDEP: {self.departure.icao} | ARR: {self.arrival} | SQUAWK: {self.departure.get_squawk()} | FINAL ALT: {self.altitude}\nAPPROVED ROUTE: {self.route} | DEP FREQ: {self.departure.get_dep_freq()}\nALTITUDE RESTRICTIONS: {self.departure.initial} | DEPARTURE PROCEDURE: {self.departure.climb}""")
