class Altitude:
    def __init__(self):
        self.alt = None
        self.get_altitude()

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
                self.alt = altitude
                break
            except ValueError:
                print("The altitude is not a valid altitude. Please enter only 3 digits")

    def __int__(self):
        return int(self.alt)

    def __str__(self):
        if int(self.alt) >= 180:
            return f'FL{self.alt}'
        if self.alt[0] == '0':
            return f'{self.alt[1]},000'
        return f'{self.alt[:2]},000'

