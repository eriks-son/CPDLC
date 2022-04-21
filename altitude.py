import airport_database


class Altitude:
    def __init__(self):
        self.alt = None

    def get_altitude(self):
        while True:
            altitude = input("Please enter your cruise altitude in hundreds of feet (for example 4,000 is 040): ")
            if len(altitude) != 3:
                print("The altitude should be 3 digits. Please type only 3 digits")
                continue
            if altitude[2] != '0':
                print("The cruise altitude must be in intervals of 1,000 ft.")
                continue
            try:
                int(altitude)
                if int(altitude) >= 410 and int(altitude) % 20 == 0:
                    print("RVSM does not apply above FL410. All altitudes must be in intervals of 2,000' starting at FL410.")
                    continue
                self.alt = altitude
                break
            except ValueError:
                print("The altitude is not a valid altitude. Please enter only 3 digits")

    def check_altitude(self, departure: str, arrival: str):
        database = airport_database.get_database()
        if -90 < database.get_track(departure, arrival) <= 90:  # This contains all East tracks (0 degrees is Due East)
            if int(self.alt) <= 410:
                if int(self.alt) % 20 == 0:
                    self.alt = str(int(self.alt) - 10)  # Drop 1,000' ft
            else:
                self.alt = "450"
        else:
            if int(self.alt) <= 410:
                if int(self.alt) % 20:
                    self.alt = str(int(self.alt) - 10)  # Drop 1,000' ft
            else:
                self.alt = "450"

    def __int__(self):
        return int(self.alt)

    def __str__(self):
        if int(self) >= 180:
            return f'FL{self.alt}'
        if self.alt[0] == '0':
            return f'{self.alt[1]},000'
        return f'{self.alt[:2]},000'
