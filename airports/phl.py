EAST = ["RUUTH", "DITCH"]
SOUTH = ["OOD", "DQO"]
WEST = ["PTW", "MXE", "STOEN", "FJC"]
ALL = EAST + SOUTH + WEST

DIGIT1 = 3
DIGIT2 = (0, 0)
DIGIT3 = (0, 7)
DIGIT4 = (1, 7)

DEP_FREQ = "124.350"


def get_initial(aircraft: str):
    if aircraft == "JET":
        return "Maintain 5,000"
    else:
        return "Maintain 3,000"
