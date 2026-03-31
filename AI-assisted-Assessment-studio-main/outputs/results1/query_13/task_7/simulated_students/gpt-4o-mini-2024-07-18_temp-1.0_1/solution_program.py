def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                elements = line.split()
                for i in range(0, len(elements) - 1, 2):
                    if i + 1 < len(elements):
                        try:
                            weight = float(elements[i + 1])
                            total_weight += weight
                            count += 1
                        except ValueError:
                            continue
            if count == 0:
                return 0.0
            average_weight = total_weight / count
            return round(average_weight, 2)
    except Exception:
        return None