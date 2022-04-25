from airport import Airport
from ops import get_ops

# Exit gates
EAST = ["RUUTH", "RBV", "DITCH", "ARD"]
SOUTH = ["OOD", "DQO"]
WEST = ["PTW", "MXE", "STOEN", "FJC"]
ALL = EAST + SOUTH + WEST

# Squawk code range
DIGIT1 = 3
DIGIT2 = (0, 0)
DIGIT3 = (0, 7)
DIGIT4 = (1, 7)


class PHL(Airport):
    def __init__(self, aircraft_type):
        super().__init__(aircraft_type)
        self.icao = "KLGA"
        self.dep_freq = "124.350"
        self.dep_runway, self.arr_runway = get_ops(self.icao)
        self.digit1 = DIGIT1
        self.digit2 = DIGIT2
        self.digit3 = DIGIT3
        self.digit4 = DIGIT4
        self.all_gates = ALL

    def get_climb(self, route):
        self.departure_procedure, self.climb = "PHL2", "PHILADELPHIA TWO (PHL2)"
        if "RBV" in str(route):
            self.departure_procedure = "PHL2 RUUTH"

    def get_initial(self):
        """Gets initial altitude instructions based off aircraft type"""
        if self.aircraft_type.category == "JET":
            self.initial = "Maintain 5,000"
        else:
            self.initial = "Maintain 3,000"
