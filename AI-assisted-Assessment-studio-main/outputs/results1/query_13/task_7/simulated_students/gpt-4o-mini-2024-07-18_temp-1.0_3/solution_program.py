def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                elements = line.split()  
                # Process only if we have a valid triplet sequence
                for i in range(1, len(elements)-1, 2):
                    weight = elements[i]
                    # Ensure that the weight can be converted to float
                    try:
                        weight_value = float(weight)
                        total_weight += weight_value
                        count += 1
                    except ValueError:
                        continue
            if count == 0:
                return 0.00
            return round(total_weight / count, 2)
    except IOError:
        return None