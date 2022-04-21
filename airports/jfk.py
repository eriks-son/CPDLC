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

DEP_FREQ = "135.900"  # Departure frequency


def get_climb(dep_rwy: str, aircraft: str, route: str):
    """Get the specific DP and climb depending on ops, aircraft type, and route"""
    if dep_rwy == "31":
        if "RBV" in route or "WHITE" in route or "DIXIE" in route:
            return "SKORR4", "SKORR FOUR (SKORR4), RNGRR TRANSITION"
        if aircraft == "JET":
            return "SKORR4", "SKORR FOUR (SKORR4), YNKEE TRANSITION"
        return "JFK5", "KENNEDY FIVE (JFK5), IDLEWILD CLIMB"
    elif dep_rwy == "4":
        return "JFK5", "KENNEDY FIVE (JFK5), EXCEPT FLY RUNWAY HEADING TO THE KENNEDY 1.5 DME, THEN TURN RIGHT HEADING 100"
    elif dep_rwy == "22":
        return "JFK5", "KENNEDY FIVE (JFK5)"
    elif dep_rwy == "13":
        if "RBV" in route or "WHITE" in route or "DIXIE" in route:
            heading = "185"
        elif "SHIPP" in route or "WAVEY" in route:
            heading = "170"
        elif "HAPIE" in route or "BETTE" in route:
            heading = "155"
        else:
            if aircraft == "JET":
                heading = "110"
            else:
                heading = "090"
        return "JFK5", f"KENNEDY FIVE (JFK5), FLY HEADING {heading}"
    raise ValueError("Unknown operations at JFK. Possible error in .get_ops() or in datis API")


def get_initial(climb: str):
    """Gets initial altitude instructions depending on departure procedure and climb"""
    if "SKORR" in climb:
        return "*Climb via SID*, TOP ALTITUDE 5,000"
    if "IDLEWILD" in climb:
        return "Maintain 2,000"
    return "Maintain 5,000"
