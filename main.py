from flight_plan import FlightPlan
from airport_database import get_database, AirportDatabase
from aircraft_type import AircraftType
from route import Route
from altitude import Altitude
from airport import Airport
from airports import ewr, jfk, lga, phl


DATABASE = get_database()

SUPPORTED_AIRPORTS = ["KEWR", "KJFK", "KLGA", "KPHL"]


def get_departure(aircraft_type: AircraftType):
    """Prompts the user for their departure airport and checks if it's supported"""
    while True:
        departure = input("Please enter your departure airport's code (ICAO): ")
        if departure in SUPPORTED_AIRPORTS:
            break
        print(f"{departure} is not a supported airport. Please choose one of the supported airports below:")
        for airport in SUPPORTED_AIRPORTS:
            print(airport)
    if departure == "KEWR":
        return ewr.EWR(aircraft_type)
    if departure == "KJFK":
        return jfk.JFK(aircraft_type)
    if departure == "KLGA":
        return lga.LGA(aircraft_type)
    return phl.PHL(aircraft_type)


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
    departure = get_departure(aircraft_type)
    arrival = get_arrival()
    altitude = Altitude()
    altitude.get_altitude()
    altitude.check_altitude(departure.icao, arrival)
    route = Route(departure, arrival)
    route.get_route()
    route.get_prd_route(altitude, aircraft_type)
    departure.get_climb(str(route))
    departure.get_initial()
    altitude.alt = route.check_altitude(altitude)
    route.check_dep_proc(departure)
    plan = FlightPlan(callsign, departure, arrival, aircraft_type, route, altitude)
    plan.get_clearance()


main()
