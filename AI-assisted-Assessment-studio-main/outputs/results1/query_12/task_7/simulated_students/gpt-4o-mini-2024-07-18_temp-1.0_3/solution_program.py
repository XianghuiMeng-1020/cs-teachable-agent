def summarize_recipes(filename):
    recipe_counts = {'stove': 0, 'oven': 0, 'no_cook': 0}
    
    with open(filename, 'r') as file:
        for line in file:
            recipe = line.strip().lower()
            if 'stove' in recipe:
                recipe_counts['stove'] += 1
            if 'oven' in recipe:
                recipe_counts['oven'] += 1
            if 'no_cook' in recipe:
                recipe_counts['no_cook'] += 1
    
    return recipe_counts