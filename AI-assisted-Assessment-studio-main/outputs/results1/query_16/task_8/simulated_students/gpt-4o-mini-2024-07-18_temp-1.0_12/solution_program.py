class MartianConverter:
    def convert_to_kilometers(self, distance):
        try:
            # Strip spaces and convert to float
            distance = float(distance.strip())
            # Check for negative values
            if distance < 0:
                return "Error: Invalid input"
            # Calculate Earth kilometers
            earth_km = distance * 2.5
            return f"{earth_km:.2f}"
        except ValueError:
            return "Error: Invalid input"