from ops import get_ops

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

DEP_FREQ = "120.400"  # Departure procedure


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


def get_climb(ops, category, route, arr):
    """Returns the DP and climb depending on the ops, aircraft type, route, and arrival runway"""
    lga7 = "LGA7"
    if ops == "4" or ops == "31":
        group1 = False
        if "WHITE" in route and category == "JET":
            group1 = True
        elif "NEWEL" in route or "ELIOT" in route or "ZIMMZ" in route or "PARKE" in route or "LANNA" in route or "BIGGY" in route:
            group1 = True

        if ops == "4":
            if group1:
                return lga7, "LA GUARDIA SEVEN (LGA7), BRONX CLIMB"
            return lga7, "LA GUARDIA SEVEN (LGA7), PELHAM CLIMB"
        else:
            if group1:
                return lga7, "LA GUARDIA SEVEN (LGA7), EXCEPT FLY HEADING 340"
            return lga7, "LA GUARDIA SEVEN (LGA7), EXCEPT FLY HEADING 360"

    elif ops == "13":
        if arr == "13":
            return lga7, "LA GUARDIA SEVEN (LGA7), FLUSHING CLIMB"
        if not coney():
            if belmont():
                return lga7, "LA GUARDIA SEVEN (LGA7), WHITESTONE CLIMB"
            return "TNNIS6", "TNNIS SIX (TNNIS6)"
        if belmont():
            if "WHITE" in route or "DIXIE" in route or "RBV" in route:
                return lga7, "LA GUARDIA SEVEN (LGA7), CONEY CLIMB"
            return lga7, "LA GUARDIA SEVEN (LGA7), WHITESTONE CLIMB"
        if "WHITE" in route or "DIXIE" in route or "RBV" in route:
            return "NTHNS5", "NTHNS FIVE (NTHNS5)"
        if "MERIT" in route or "GREKI" in route or "BAYYS" in route or "BDR" in route:
            return "TNNIS6", "TNNIS SIX (TNNIS6)"
        if arr == "4":
            return "TNNIS6", "TNNIS SIX (TNNIS6)"
        return "GLDMN7", "GLDMN SEVEN (GLDMN7)"
    elif ops == "22":
        if coney() and ("WHITE" in route or "DIXIE" in route or "RBV" in route):
            return "HOPEA3", "HOPEA THREE (HOPEA3)"
        return "JUTES3", "JUTES THREE (JUTES3)"
    raise ValueError("Unknown operations at LGA. Possible error in .get_ops() or in datis API")


def get_initial(procedure, climb):
    """Returns the initial altitude instructions based on the DP and climb"""
    if procedure == "LGA7" and "CONEY" not in climb:
        return "Maintain 5,000"
    return "*CLIMB VIA SID*, TOP ALTITUDE 5,000"
