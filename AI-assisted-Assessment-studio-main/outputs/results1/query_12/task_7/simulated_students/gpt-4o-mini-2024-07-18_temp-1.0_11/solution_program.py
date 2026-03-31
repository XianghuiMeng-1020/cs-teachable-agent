def summarize_recipes(filename):
    stove_count = 0
    oven_count = 0
    no_cook_count = 0
    
    with open(filename, 'r') as file:
        for line in file:
            description = line.strip().lower()
            if 'stove' in description:
                stove_count += 1
            if 'oven' in description:
                oven_count += 1
            if 'no_cook' in description:
                no_cook_count += 1
    
    return {'stove': stove_count, 'oven': oven_count, 'no_cook': no_cook_count}