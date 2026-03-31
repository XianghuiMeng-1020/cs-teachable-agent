def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                elements = line.split()
                # Check if the line has an even number of elements (pairs of ingredient and weight)
                if len(elements) % 2 == 0 and len(elements) > 2:
                    # Iterate over the weight elements (which are on odd indices)
                    for i in range(1, len(elements), 2):
                        try:
                            weight = float(elements[i])
                            total_weight += weight
                            count += 1
                        except ValueError:
                            continue
            return round(total_weight / count, 2) if count > 0 else 0.0
    except Exception:
        return None