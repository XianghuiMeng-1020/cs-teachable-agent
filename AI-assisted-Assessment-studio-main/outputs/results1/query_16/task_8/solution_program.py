class MartianConverter:
    def convert_to_kilometers(self, distance):
        try:
            number = float(distance.strip())
            if number < 0:
                return "Error: Invalid input"
            result = number * 2.5
            return f"{result:.2f}"
        except ValueError:
            return "Error: Invalid input"