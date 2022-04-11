class Route:
    """Reads route from the flight plan and checks the PRD database to see if changes must be made"""

    def __init__(self, rt: str, aircraft_type: str, altitude: int):
        """Initializes the Route object"""
        self.route = rt
        self.aircraft_type = aircraft_type
        self.altitude = altitude

    def __str__(self):
        """Returns just the route (the rest is only for PRD purposes)"""
        return self.route


