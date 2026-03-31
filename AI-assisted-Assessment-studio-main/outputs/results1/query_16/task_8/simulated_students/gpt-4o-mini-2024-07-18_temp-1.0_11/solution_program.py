class MartianConverter:
    def convert_to_kilometers(self, distance):
        try:
            # Strip any leading/trailing whitespace and convert to float
            distance = float(distance.strip())
            if distance < 0:
                return "Error: Invalid input"
            # Convert Martian distance to Earth kilometers
            earth_kilometers = distance * 2.5
            return f"{earth_kilometers:.2f}"
        except ValueError:
            return "Error: Invalid input"