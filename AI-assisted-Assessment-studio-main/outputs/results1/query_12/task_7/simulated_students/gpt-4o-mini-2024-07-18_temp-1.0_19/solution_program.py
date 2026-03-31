def summarize_recipes(filename):
    stove_count = 0
    oven_count = 0
    no_cook_count = 0

    with open(filename, 'r') as file:
        for line in file:
            line = line.lower()  # Normalize to lowercase for consistency
            if 'stove' in line:
                stove_count += 1
            if 'oven' in line:
                oven_count += 1
            if 'no_cook' in line:
                no_cook_count += 1

    return {'stove': stove_count, 'oven': oven_count, 'no_cook': no_cook_count}