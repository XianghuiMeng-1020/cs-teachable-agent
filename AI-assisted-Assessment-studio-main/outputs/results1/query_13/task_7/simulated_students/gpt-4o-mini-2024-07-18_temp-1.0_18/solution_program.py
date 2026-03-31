def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                elements = line.split()  # Split the line into parts
                # Ensure that we have a correct number of elements (multiple of 3)
                if len(elements) % 3 == 0:
                    for i in range(1, len(elements), 3):  # Start from 1, get every 3rd element
                        weight = elements[i]  # weight is at index i
                        total_weight += int(weight)
                        count += 1
            if count > 0:
                return round(total_weight / count, 2)
            else:
                return 0.00
    except IOError:
        return None