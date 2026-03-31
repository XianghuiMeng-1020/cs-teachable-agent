def summarize_recipes(filename):
    summary = {'stove': 0, 'oven': 0, 'no_cook': 0}
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip().lower()
            if 'stove' in line:
                summary['stove'] += 1
            if 'oven' in line:
                summary['oven'] += 1
            if 'no_cook' in line:
                summary['no_cook'] += 1

    return summary