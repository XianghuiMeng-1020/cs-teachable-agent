def calculate_ingredient_amounts(ingredient_list, desired_servings):
    adjusted_ingredients = []
    for ingredient in ingredient_list:
        name, amount = ingredient.split(':')
        amount_value = int(amount[:-2])
        amount_unit = amount[-2:]
        new_amount = amount_value * desired_servings
        adjusted_ingredients.append(f'{name}:{new_amount}{amount_unit}')
    return adjusted_ingredients