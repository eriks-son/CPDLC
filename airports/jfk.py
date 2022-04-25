from airport import Airport
import ops


# Exit gates
EAST = ["GREKI", "MERIT", "BAYYS", "BDR"]
WATER = ["BETTE", "HAPIE", "SHIPP", "WAVEY"]
SOUTHWEST = ["RBV", "WHITE", "DIXIE"]
NORTH = ["GAYEL", "HAAYS", "NEION", "COATE"]
ALL = EAST + WATER + SOUTHWEST + NORTH

# Squawk code range
DIGIT1 = 1
DIGIT2 = (5, 6)
DIGIT3 = (0, 7)
DIGIT4 = (1, 7)


class JFK(Airport):
    def __init__(self, aircraft_type):
        super().__init__(aircraft_type)
        self.icao = "KJFK"
        self.dep_freq = "135.900"
        self.dep_runway, self.arr_runway = ops.get_ops(self.icao)
        self.digit1 = DIGIT1
        self.digit2 = DIGIT2
        self.digit3 = DIGIT3
        self.digit4 = DIGIT4
        self.all_gates = ALL

    def get_climb(self, route: str):
        """Get the specific DP and climb depending on ops, aircraft type, and route"""
        if self.dep_runway == "31":
            if "RBV" in route or "WHITE" in route or "DIXIE" in route:
                self.departure_procedure, self.climb = "SKORR4", "SKORR FOUR (SKORR4), RNGRR TRANSITION"
            elif self.aircraft_type.category == "JET":
                self.departure_procedure, self.climb = "SKORR4", "SKORR FOUR (SKORR4), YNKEE TRANSITION"
            else:
                self.departure_procedure, self.climb = "JFK5", "KENNEDY FIVE (JFK5), IDLEWILD CLIMB"
        elif self.dep_runway == "4":
            self.departure_procedure, self.climb = "JFK5", "KENNEDY FIVE (JFK5), EXCEPT FLY RUNWAY HEADING TO THE KENNEDY 1.5 DME, THEN TURN RIGHT HEADING 100"
        elif self.dep_runway == "22":
            self.departure_procedure, self.climb = "JFK5", "KENNEDY FIVE (JFK5)"
        elif self.dep_runway == "13":
            if "RBV" in route or "WHITE" in route or "DIXIE" in route:
                heading = "185"
            elif "SHIPP" in route or "WAVEY" in route:
                heading = "170"
            elif "HAPIE" in route or "BETTE" in route:
                heading = "155"
            else:
                if self.aircraft_type.category == "JET":
                    heading = "110"
                else:
                    heading = "090"
            self.departure_procedure, self.climb = "JFK5", f"KENNEDY FIVE (JFK5), FLY HEADING {heading}"
        else:
            raise ValueError("Unknown operations at JFK. Possible error in .get_ops() or in datis API")

    def get_initial(self):
        """Gets initial altitude instructions depending on departure procedure and climb"""
        if "SKORR" in self.climb:
            self.initial = "*Climb via SID*, TOP ALTITUDE 5,000"
        elif "IDLEWILD" in self.climb:
            self.initial = "Maintain 2,000"
        else:
            self.initial = "Maintain 5,000"
