def recipe_summary(recipe):
    summary = {}
    lines = recipe.strip().split('\n')
    for line in lines:
        if ':' in line:
            ingredient, quantity_unit = line.split(':')
            quantity, unit = quantity_unit.split()[:2]
            summary[ingredient.strip()] = {'quantity': quantity.strip(), 'unit': unit.strip()}
    return summary