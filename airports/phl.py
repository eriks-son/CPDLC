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

DEP_FREQ = "124.350"  # Departure frequency


def get_initial(aircraft: str):
    """Gets initial altitude instructions based off aircraft type"""
    if aircraft == "JET":
        return "Maintain 5,000"
    else:
        return "Maintain 3,000"
