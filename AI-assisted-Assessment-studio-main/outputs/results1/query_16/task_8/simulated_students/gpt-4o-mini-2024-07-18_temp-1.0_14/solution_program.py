class MartianConverter:
    def convert_to_kilometers(self, distance):
        try:
            distance = distance.strip()
            if not distance:
                raise ValueError("Invalid input")
            value = float(distance)
            if value < 0:
                raise ValueError("Invalid input")
            earth_kilometers = value * 2.5
            return f'{earth_kilometers:.2f}'
        except ValueError:
            return "Error: Invalid input"