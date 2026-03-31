class MartianConverter:
    def convert_to_kilometers(self, distance):
        try:
            cleaned_distance = distance.strip()  
            if cleaned_distance == "" or float(cleaned_distance) < 0:
                return "Error: Invalid input"
            numeric_distance = float(cleaned_distance)
            kilometers = numeric_distance * 2.5
            return f"{kilometers:.2f}"
        except ValueError:
            return "Error: Invalid input"