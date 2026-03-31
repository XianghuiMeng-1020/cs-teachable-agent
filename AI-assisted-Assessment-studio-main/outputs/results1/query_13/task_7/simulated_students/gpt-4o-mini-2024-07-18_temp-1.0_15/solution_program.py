def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                elements = line.split()
                # Check if we have a valid format: at least ingredient-weight-ingredient
                for i in range(1, len(elements)-1, 2):
                    try:
                        weight = float(elements[i])  # Convert weight to float
                        total_weight += weight
                        count += 1
                    except (ValueError, IndexError):
                        continue  # Skip if not a number or index out of range
            if count == 0:
                return 0.0  # Prevent division by zero
            average_weight = total_weight / count
            return round(average_weight, 2)
    except IOError:
        return None