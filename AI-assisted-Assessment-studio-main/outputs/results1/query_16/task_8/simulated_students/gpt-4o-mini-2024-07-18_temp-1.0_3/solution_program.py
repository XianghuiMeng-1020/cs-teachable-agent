class MartianConverter:
    def convert_to_kilometers(self, distance):
        try:
            # Strip any leading/trailing whitespace and convert to float
            cleaned_distance = float(distance.strip())
            if cleaned_distance < 0:
                return "Error: Invalid input"
            kilometers = cleaned_distance * 2.5
            return f"{kilometers:.2f}"
        except (ValueError, TypeError):
            return "Error: Invalid input"