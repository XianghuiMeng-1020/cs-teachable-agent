def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            valid_weights_count = 0
            for line in file:
                elements = line.split()
                if len(elements) >= 3:
                    for i in range(1, len(elements), 2):
                        if i < len(elements):
                            try:
                                weight = float(elements[i])
                                total_weight += weight
                                valid_weights_count += 1
                            except ValueError:
                                continue
        if valid_weights_count == 0:
            return 0.0
        return round(total_weight / valid_weights_count, 2)
    except IOError:
        return None