def recipe_summary(recipe):
    summary = {}
    lines = recipe.strip().split('\n')
    for line in lines:
        ingredient, amount = line.split(': ')
        quantity, unit = amount.split(' ')
        summary[ingredient] = {'quantity': float(quantity), 'unit': unit}
    return summary