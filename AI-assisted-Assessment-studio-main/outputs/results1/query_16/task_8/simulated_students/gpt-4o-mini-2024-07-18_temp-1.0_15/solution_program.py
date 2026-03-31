class MartianConverter:
    def convert_to_kilometers(self, distance):
        try:
            distance = distance.strip()
            value = float(distance)
            if value < 0:
                return "Error: Invalid input"
            kilometers = value * 2.5
            return f'{kilometers:.2f}'
        except ValueError:
            return "Error: Invalid input"