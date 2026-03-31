def calculate_ingredient_amounts(ingredient_list, desired_servings):
    adjusted_ingredient_list = []
    for ingredient in ingredient_list:
        name, amount = ingredient.split(':')
        amount_value = int(''.join(filter(str.isdigit, amount)))
        amount_unit = ''.join(filter(str.isalpha, amount))
        adjusted_amount = amount_value * desired_servings
        adjusted_ingredient_list.append(f'{name}:{adjusted_amount}{amount_unit}')
    return adjusted_ingredient_list