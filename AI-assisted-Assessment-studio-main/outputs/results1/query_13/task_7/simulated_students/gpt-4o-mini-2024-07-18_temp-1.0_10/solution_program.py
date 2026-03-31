def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                elements = line.split()
                for i in range(1, len(elements), 2):  # Check weights
                    if i < len(elements) - 1:
                        try:
                            weight = float(elements[i])
                            total_weight += weight
                            count += 1
                        except ValueError:
                            pass  # Ignore invalid weight
            if count > 0:
                return round(total_weight / count, 2)
            else:
                return 0.0
    except IOError:
        return None