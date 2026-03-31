def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                parts = line.split()
                for i in range(1, len(parts), 2):
                    if i + 1 < len(parts):
                        try:
                            weight = float(parts[i])
                            total_weight += weight
                            count += 1
                        except ValueError:
                            continue
            return round(total_weight / count, 2) if count > 0 else 0.0
    except IOError:
        return None