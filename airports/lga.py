from ops import get_ops
from airport import Airport


# Exit gates
EAST = ["GREKI", "MERIT", "BAYYS", "BDR"]
SOUTH = ["SHIPP", "WAVEY", "DIXIE", "WHITE"]
NORTH = ["GAYEL", "HAAYS", "NEION", "COATE"]
WEST = ["NEWEL", "ELIOT", "ZIMMZ", "PARKE", "LANNA", "LANNA"]
ALL = EAST + SOUTH + NORTH + WEST

# Squawk code range
DIGIT1 = 2
DIGIT2 = (1, 1)
DIGIT3 = (0, 6)
DIGIT4 = (1, 7)


def belmont():
    """Returns True if LGA owns the Belmont airspace, False otherwise"""
    dep, arr = get_ops("KJFK")
    if dep == "22" or arr == "22":
        return False
    return True


def coney():
    """Returns True if LGA owns the Coney airspace, False otherwise"""
    dep, arr = get_ops("KJFK")
    if dep == "31" or arr == "31" or dep == "13" or arr == "13":
        return False
    return True


class LGA(Airport):
    def __init__(self, aircraft_type):
        super().__init__(aircraft_type)
        self.icao = "KLGA"
        self.dep_freq = "120.400"
        self.dep_runway, self.arr_runway = get_ops(self.icao)
        self.digit1 = DIGIT1
        self.digit2 = DIGIT2
        self.digit3 = DIGIT3
        self.digit4 = DIGIT4
        self.all_gates = ALL

    def get_climb(self, route):
        """Returns the DP and climb depending on the ops, aircraft type, route, and arrival runway"""
        lga7 = "LGA7"
        if self.dep_runway == "4" or self.dep_runway == "31":
            group1 = False
            if "WHITE" in route and self.aircraft_type.category == "JET":
                group1 = True
            elif "NEWEL" in route or "ELIOT" in route or "ZIMMZ" in route or "PARKE" in route or "LANNA" in route or "BIGGY" in route:
                group1 = True

            if self.dep_runway == "4":
                if group1:
                    self.departure_procedure, self.climb = lga7, "LA GUARDIA SEVEN (LGA7), BRONX CLIMB"
                else:
                    self.departure_procedure, self.climb = lga7, "LA GUARDIA SEVEN (LGA7), PELHAM CLIMB"
            else:
                if group1:
                    self.departure_procedure, self.climb = lga7, "LA GUARDIA SEVEN (LGA7), EXCEPT FLY HEADING 340"
                else:
                    self.departure_procedure, self.climb = lga7, "LA GUARDIA SEVEN (LGA7), EXCEPT FLY HEADING 360"

        elif self.dep_runway == "13":
            if self.arr_runway == "13":
                self.departure_procedure, self.climb = lga7, "LA GUARDIA SEVEN (LGA7), FLUSHING CLIMB"
            else:
                if not coney():
                    if belmont():
                        self.departure_procedure, self.climb = lga7, "LA GUARDIA SEVEN (LGA7), WHITESTONE CLIMB"
                    else:
                        self.departure_procedure, self.climb = "TNNIS6", "TNNIS SIX (TNNIS6)"
                elif belmont():
                    if "WHITE" in route or "DIXIE" in route or "RBV" in route:
                        self.departure_procedure, self.climb = lga7, "LA GUARDIA SEVEN (LGA7), CONEY CLIMB"
                    else:
                        self.departure_procedure, self.climb = lga7, "LA GUARDIA SEVEN (LGA7), WHITESTONE CLIMB"
                elif "WHITE" in route or "DIXIE" in route or "RBV" in route:
                    self.departure_procedure, self.climb = "NTHNS5", "NTHNS FIVE (NTHNS5)"
                elif "MERIT" in route or "GREKI" in route or "BAYYS" in route or "BDR" in route:
                    self.departure_procedure, self.climb = "TNNIS6", "TNNIS SIX (TNNIS6)"
                elif self.arr_runway == "4":
                    self.departure_procedure, self.climb = "TNNIS6", "TNNIS SIX (TNNIS6)"
                else:
                    self.departure_procedure, self.climb = "GLDMN7", "GLDMN SEVEN (GLDMN7)"
        elif self.dep_runway == "22":
            if coney() and ("WHITE" in route or "DIXIE" in route or "RBV" in route):
                self.departure_procedure, self.climb = "HOPEA3", "HOPEA THREE (HOPEA3)"
            else:
                self.departure_procedure, self.climb = "JUTES3", "JUTES THREE (JUTES3)"
        else:
            raise ValueError("Unknown operations at LGA. Possible error in .get_ops() or in datis API")

    def get_initial(self):
        """Returns the initial altitude instructions based on the DP and climb"""
        if self.departure_procedure == "LGA7" and "CONEY" not in self.climb:
            self.initial = "Maintain 5,000"
        else:
            self.initial = "*CLIMB VIA SID*, TOP ALTITUDE 5,000"
