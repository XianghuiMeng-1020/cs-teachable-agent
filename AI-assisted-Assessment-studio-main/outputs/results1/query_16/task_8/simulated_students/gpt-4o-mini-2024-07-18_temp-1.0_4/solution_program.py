class MartianConverter:
    def convert_to_kilometers(self, distance):
        try:
            # Strip the input of extra whitespace
            distance = distance.strip()
            # Convert to float
            value = float(distance)
            # Check for negative value
            if value < 0:
                return "Error: Invalid input"
            # Conversion rate
            kilometers = value * 2.5
            # Return rounded result
            return f'{kilometers:.2f}'
        except ValueError:
            return "Error: Invalid input"