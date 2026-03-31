def calculate_ingredient_amounts(ingredient_list, desired_servings):
    adjusted_ingredients = []
    for ingredient in ingredient_list:
        name, amount = ingredient.split(':')
        amount_value = int(''.join(filter(str.isdigit, amount)))
        unit = ''.join(filter(str.isalpha, amount))
        adjusted_amount = amount_value * desired_servings
        adjusted_ingredients.append(f'{name}:{adjusted_amount}{unit}')
    return adjusted_ingredients