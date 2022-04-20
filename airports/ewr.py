def get_initial(dep_rwy: str):
    if dep_rwy == "4" or dep_rwy == "11":
        return "*Climb via SID*, except maintain 3,000"
    elif dep_rwy == "22":
        return "Maintain 2,500"
    elif dep_rwy == "29":
        return "Maintain 5,000"
    raise ValueError("Unknown operations at EWR. Possible error in .get_ops() or in datis API")
