def recipe_summary(recipe):
    summary = {}
    lines = recipe.strip().split('\n')
    for line in lines:
        ingredient, quantity_unit = line.split(': ')
        quantity, unit = quantity_unit.split(' ')
        summary[ingredient] = {'quantity': quantity, 'unit': unit}
    return summary