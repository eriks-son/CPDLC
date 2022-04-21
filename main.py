from flight_plan import FlightPlan
from airport_database import get_database, AirportDatabase
from aircraft_type import AircraftType
from route import Route
from airport import Airport
from altitude import Altitude


DATABASE = get_database()


def get_arrival():
    """
    Prompts the user for their arrival airport and checks if it is in the airport database (.dat file)
    """
    while True:
        arrival = input("Please enter your arrival airport's code (ICAO): ")
        if DATABASE.is_in_list(arrival):
            return arrival
        if arrival == "0":
            raise Exception("Unsupported arrival airport. User requested to exit")
        print(f"{arrival} is not a supported arrival airport. It may be too small of an airport to be supported.")
        print("Please enter a supported airport or type 0 to exit")


def main():
    callsign = input("Please enter your callsign (in ICAO form): ")  # No data validation necessary (it's just a callsign)
    aircraft_type = AircraftType()
    aircraft_type.get_aircraft_type()
    departure = Airport()
    arrival = get_arrival()
    altitude = Altitude()
    altitude.get_altitude()
    altitude.check_altitude(departure.icao, arrival)
    route = Route(departure, arrival)
    route.get_route()
    route.get_prd_route(altitude, aircraft_type)
    departure.specific_airport(route, aircraft_type)
    altitude.alt = route.check_altitude(altitude)
    route.check_dep_proc(departure)
    plan = FlightPlan(callsign, departure, arrival, aircraft_type, route, altitude)
    plan.get_clearance()


main()
