def get_climb(dep_rwy: str, aircraft: str, route: str):
    if dep_rwy == "31":
        if "RBV" in route or "WHITE" in route or "DIXIE" in route:
            return "SKORR4", "SKORR FOUR (SKORR4), RNGRR TRANSITION"
        if aircraft == "JET":
            return "SKORR4", "SKORR FOUR (SKORR4), YNKEE TRANSITION"
        return "JFK5", "KENNEDY FIVE (JFK5), IDLEWILD CLIMB"
    if dep_rwy == "4":
        return "JFK5", "KENNEDY FIVE (JFK5), EXCEPT FLY RUNWAY HEADING TO THE KENNEDY 1.5 DME, THEN TURN RIGHT HEADING 100"
    if dep_rwy == "22":
        return "JFK5", "KENNEDY FIVE (JFK5)"
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


def get_initial(climb: str):
    if "SKORR" in climb:
        return "*Climb via SID*, TOP ALTITUDE 5,000"
    if "IDLEWILD" in climb:
        return "Maintain 2,000"
    return "Maintain 5,000"
