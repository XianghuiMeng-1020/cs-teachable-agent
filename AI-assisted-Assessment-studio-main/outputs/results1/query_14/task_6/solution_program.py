def recipe_summary(recipe):
    summary = {}
    lines = recipe.split('\n')
    for line in lines:
        if line.strip():
            ingredient, details = line.split(': ')
            quantity, unit = details.split(' ')
            summary[ingredient] = {'quantity': quantity, 'unit': unit}
    return summary
