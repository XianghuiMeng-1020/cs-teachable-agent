def recipe_summary(recipe):
    summary = {}
    lines = recipe.strip().split('\n')
    for line in lines:
        ingredient, details = line.split(':')
        quantity, unit = details.split(' ')
        summary[ingredient.strip()] = {'quantity': quantity.strip(), 'unit': unit.strip()}
    return summary