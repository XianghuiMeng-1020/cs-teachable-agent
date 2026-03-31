def recipe_summary(recipe):
    summary = {}
    lines = recipe.strip().split('\n')
    for line in lines:
        ingredient, info = line.split(':')
        quantity, unit = info.split() 
        summary[ingredient] = {'quantity': float(quantity), 'unit': unit}
    return summary