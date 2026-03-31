def calculate_ingredient_amounts(ingredient_list, desired_servings):
    adjusted_ingredients = []
    for ingredient in ingredient_list:
        name, amount = ingredient.split(':')
        unit = amount[-2:]
        quantity = int(amount[:-2])
        adjusted_quantity = quantity * desired_servings
        adjusted_ingredients.append(f'{name}:{adjusted_quantity}{unit}')
    return adjusted_ingredients