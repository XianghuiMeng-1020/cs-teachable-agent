def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                elements = line.split()
                for i in range(1, len(elements), 2):
                    if i+1 < len(elements):
                        try:
                            weight = float(elements[i])
                            total_weight += weight
                            count += 1
                        except ValueError:
                            continue
            if count > 0:
                return round(total_weight / count, 2)
            else:
                return 0.0
    except FileNotFoundError:
        return None