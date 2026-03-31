def recipe_summary(recipe):
    summary = {}
    lines = recipe.strip().split('\n')
    for line in lines:
        ingredient, quantity_unit = line.split(':')
        quantity, unit = quantity_unit.split()[:2]
        summary[ingredient.strip()] = {'quantity': int(quantity), 'unit': unit.strip()}
    return summary