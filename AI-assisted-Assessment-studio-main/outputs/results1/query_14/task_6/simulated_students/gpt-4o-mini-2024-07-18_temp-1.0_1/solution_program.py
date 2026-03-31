def recipe_summary(recipe):
    summary = {}
    lines = recipe.strip().split('\n')
    for line in lines:
        ingredient, quantity_unit = line.split(':')
        quantity, unit = quantity_unit.strip().split(' ')
        summary[ingredient.strip()] = {'quantity': float(quantity), 'unit': unit.strip()}
    return summary