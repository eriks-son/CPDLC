# List of ICAO type identifiers for different standard aircraft
JETS = ["A319", "A320", "A318", "A321", "A20N", "A300", "A330", "A332", "A333", "A338", "A339", "A340", "A342", "A343",
        "A345", "A346", "A350", "A359", "A35K", "A380", "A388", "B737", "B738", "B739", "B38M", "B39M", "B744", "B747",
        "B748", "B752", "B753", "B762", "B763", "B764", "B772", "B773", "MD11", "E135", "E140", "E145", "E170", "E175",
        "E190", "E195", "CRJ1", "CRJ2", "CRJ7", "CRJ9", "CRJX", "BCS1", "BCS2"]
PROPS = ["C172", "C152", "C182", "C206", "C210", "PA42", "PA62", "BE35", "B350", "C208"]
TURBOPROPS = ["DH8A", "DH8B", "DH8C", "DH8D", "TBM9", "PC12"]


class AircraftType:
    def __init__(self):
        self.aircraft_type = None
        self.category = None
        self.opposite = None
        self.turbo = False

    def get_aircraft_type(self):
        """
        Prompts the user for an aircraft type. Checks if it is in the hardcoded list
        If it's not in the list, the user can use it as a custom type and is prompted for the category of aircraft
        """
        while True:
            self.aircraft_type = input("Please enter your aircraft type: ")
            if self.aircraft_type in JETS or self.aircraft_type in PROPS or self.aircraft_type in TURBOPROPS:
                if self.aircraft_type in JETS:
                    self.category = "JET"
                    self.opposite = "PROP"
                else:
                    self.category = "PROP"
                    self.opposite = "JET"
                    if self.aircraft_type in TURBOPROPS:
                        self.turbo = True
                break
            else:
                print("Your aircraft type is not recognized. Would you like to use a custom aircraft?")
                custom = input("Enter 1 to use a custom aircraft or anything else to try a new type: ")
                if custom != 1:
                    continue
                print("Firstly is your aircraft a jet or a prop?")
                is_jet = input("If your aircraft is a jet, enter 1. If it's not, enter anything else: ")
                if is_jet:
                    self.category = "JET"
                    self.opposite = "PROP"
                    break
                self.category = "PROP"
                self.opposite = "JET"
                print("Is your aircraft a turboprop or a regular piston aircraft?")
                is_turbo = input("If your aircraft is a turboprop, enter 1. If not, enter anything else: ")
                if is_turbo:
                    self.turbo = True
                break

    def __str__(self):
        return self.aircraft_type
