def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                elements = line.split()  # Split line into elements
                if len(elements) >= 3:
                    for i in range(1, len(elements), 2):  # Check every weight (odd index)
                        try:
                            weight = float(elements[i])  # Convert weight to float
                            total_weight += weight
                            count += 1
                        except ValueError:
                            pass  # Skip non-float weights
            return round(total_weight / count, 2) if count > 0 else 0.0
    except (FileNotFoundError, IOError):
        return None