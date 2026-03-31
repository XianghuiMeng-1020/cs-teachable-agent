def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                parts = line.split()
                if len(parts) % 3 == 0:
                    for i in range(1, len(parts), 3):
                        total_weight += float(parts[i])
                        count += 1
            if count > 0:
                return round(total_weight / count, 2)
            return None
    except Exception:
        return None
