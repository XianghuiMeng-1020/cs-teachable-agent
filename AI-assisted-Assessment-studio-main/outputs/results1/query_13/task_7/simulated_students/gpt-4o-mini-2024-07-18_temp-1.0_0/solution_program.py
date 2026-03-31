def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            ingredient_count = 0
            for line in file:
                elements = line.split()
                if len(elements) < 3:
                    continue
                for i in range(1, len(elements), 2):
                    try:
                        weight = float(elements[i])
                        total_weight += weight
                        ingredient_count += 1
                    except ValueError:
                        continue
            if ingredient_count == 0:
                return 0.0
            average_weight = total_weight / ingredient_count
            return round(average_weight, 2)
    except IOError:
        return None