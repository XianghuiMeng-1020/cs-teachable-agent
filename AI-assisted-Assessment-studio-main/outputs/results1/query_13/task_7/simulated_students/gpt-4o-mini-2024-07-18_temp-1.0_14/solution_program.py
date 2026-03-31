def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                elements = line.split()  
                if len(elements) < 3 or len(elements) % 3 != 0:
                    continue
                for i in range(1, len(elements), 3):
                    try:
                        weight = float(elements[i])
                        total_weight += weight
                        count += 1
                    except ValueError:
                        continue
            if count == 0:
                return 0.0
            return round(total_weight / count, 2)
    except IOError:
        return None