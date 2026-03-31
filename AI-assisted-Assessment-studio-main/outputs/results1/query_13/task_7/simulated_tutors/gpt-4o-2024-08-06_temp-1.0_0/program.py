def calculate_average_ingredient_weight(filename):
    try:
        with open(filename, 'r') as file:
            total_weight = 0
            count = 0
            for line in file:
                elements = line.split()
                # Each valid line must have at least 3 elements and odd number of elements
                if len(elements) >= 3 and len(elements) % 2 == 1:
                    for i in range(1, len(elements), 2):
                        try:
                            weight = float(elements[i])
                            total_weight += weight
                            count += 1
                        except ValueError:
                            # If conversion fails, skip this entry
                            continue
            if count == 0:
                return None
            return round(total_weight / count, 2)
    except FileNotFoundError:
        return None

# The program will use loops to iterate over lines and elements, variables to store cumulative weights and count,
# and exception handling to manage file errors and invalid data.