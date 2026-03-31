class MartianConverter:
    def convert_to_kilometers(self, distance):
        try:
            # Strip spaces and convert to float
            distance = float(distance.strip())
            if distance < 0:
                return "Error: Invalid input"
            # Convert to kilometers
            kilometers = distance * 2.5
            return f"{kilometers:.2f}"
        except ValueError:
            return "Error: Invalid input"