def summarize_recipes(filename):
    counts = {'stove': 0, 'oven': 0, 'no_cook': 0}
    with open(filename, 'r') as file:
        for line in file:
            line_lower = line.lower()
            if 'stove' in line_lower:
                counts['stove'] += 1
            if 'oven' in line_lower:
                counts['oven'] += 1
            if 'no_cook' in line_lower:
                counts['no_cook'] += 1
    return counts