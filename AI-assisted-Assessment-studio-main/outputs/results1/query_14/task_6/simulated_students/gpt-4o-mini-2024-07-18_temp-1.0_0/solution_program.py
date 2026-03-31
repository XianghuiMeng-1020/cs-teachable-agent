def recipe_summary(recipe):
    result = {}
    lines = recipe.strip().split('\n')
    for line in lines:
        ingredient, quantity_unit = line.split(':')
        quantity, unit = quantity_unit.strip().split(' ')
        result[ingredient.strip()] = {'quantity': float(quantity), 'unit': unit}
    return result