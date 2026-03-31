def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            ingredient_count = 0
            for line in file:
                parts = line.split()
                if len(parts) % 3 == 0:
                    for i in range(1, len(parts), 3):
                        try:
                            weight = float(parts[i])
                            total_weight += weight
                            ingredient_count += 1
                        except ValueError:
                            continue
            if ingredient_count > 0:
                return round(total_weight / ingredient_count, 2)
            else:
                return 0.00
    except IOError:
        return None