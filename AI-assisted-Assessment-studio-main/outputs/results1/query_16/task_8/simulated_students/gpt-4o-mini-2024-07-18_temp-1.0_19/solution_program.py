class MartianConverter:
    def convert_to_kilometers(self, distance):
        try:
            # Remove extra spaces and convert to float
            cleaned_distance = distance.strip()
            value = float(cleaned_distance)
            if value < 0:
                return "Error: Invalid input"
            # Convert to kilometers
            kilometers = value * 2.5
            return f"{kilometers:.2f}"
        except ValueError:
            return "Error: Invalid input"