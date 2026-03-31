def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                elements = line.split()  
                # Check if we have a valid triplet (ingredient, weight, next ingredient)
                if len(elements) >= 3:
                    for i in range(1, len(elements), 2):  # Check weights at odd indices
                        weight = elements[i]
                        try:
                            weight_value = float(weight)
                            total_weight += weight_value
                            count += 1
                        except ValueError:
                            continue  # ignore non-numeric weights
            if count == 0:
                return 0.00  # Return 0.00 if no valid weights
            average_weight = total_weight / count
            return round(average_weight, 2)
    except (FileNotFoundError, IOError):
        return None