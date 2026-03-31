class MartianConverter:
    def convert_to_kilometers(self, distance):
        # Strip whitespace from the input
        distance = distance.strip()
        try:
            # Convert to float
            martian_distance = float(distance)
            if martian_distance < 0:
                raise ValueError("Negative distance not allowed")
            # Conversion factor
            earth_distance = martian_distance * 2.5
            # Return formatted string
            return f"{earth_distance:.2f}"
        except ValueError:
            return "Error: Invalid input"