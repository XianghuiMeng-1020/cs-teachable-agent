class MartianConverter:
    def convert_to_kilometers(self, distance):
        try:
            # Strip any leading/trailing whitespace
            distance = distance.strip()
            # Convert to float
            distance_value = float(distance)
            # Check for negative values
            if distance_value < 0:
                return "Error: Invalid input"
            # Perform conversion
            kilometers = distance_value * 2.5
            # Return rounded result as string
            return f"{kilometers:.2f}"
        except ValueError:
            return "Error: Invalid input"