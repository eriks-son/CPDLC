from airport import Airport
import ops


# Exit gates
EAST = ["MERIT", "GREKI", "BAYYS", "BDR"]
SOUTH = ["WHITE", "DIXIE", "WAVEY", "SHIPP"]
NORTH = ["GAYEL", "HAAYS", "NEION", "COATE"]
WEST = ["NEWEL", "ELIOT", "ZIMMZ", "PARKE", "LANNA", "BIGGY"]
ALL = EAST + SOUTH + NORTH + WEST

# Squawk code range
DIGIT1 = 2
DIGIT2 = (3, 3)
DIGIT3 = (0, 7)
DIGIT4 = (1, 7)


class EWR(Airport):
    def __init__(self, aircraft_type):
        super().__init__(aircraft_type)
        self.icao = "KEWR"
        self.dep_freq = "119.200"
        self.dep_runway, self.arr_runway = ops.get_ops(self.icao)
        self.digit1 = DIGIT1
        self.digit2 = DIGIT2
        self.digit3 = DIGIT3
        self.digit4 = DIGIT4
        self.all_gates = ALL

    def get_initial(self):
        """
        Returns the initial altitude instructions depending on config
        """
        if self.dep_runway == "4" or self.dep_runway == "11":
            return "*Climb via SID*, except maintain 3,000"
        elif self.dep_runway == "22":
            return "Maintain 2,500"
        elif self.dep_runway == "29":
            return "Maintain 5,000"
        raise ValueError("Unknown operations at EWR. Possible error in .get_ops() or in datis API")

    def get_climb(self, route):
        """
        The EWR4 is always the preferred departure procedure
        Will add 'ELVAE COL' or 'BREZY V39 CMK' to the beginning of a route before the exit gate if applicable
        """
        self.climb = "NEWARK FOUR (EWR4)"
        self.departure_procedure = "EWR4"
        if "WHITE" in str(route) or "DIXIE" in str(route):
            self.departure_procedure = self.departure_procedure + " ELVAE COL"
        if self.aircraft_type.category == "PROP":
            for gate in EAST:
                if gate in str(route):
                    self.departure_procedure = self.departure_procedure + " BREZY V39 CMK"
