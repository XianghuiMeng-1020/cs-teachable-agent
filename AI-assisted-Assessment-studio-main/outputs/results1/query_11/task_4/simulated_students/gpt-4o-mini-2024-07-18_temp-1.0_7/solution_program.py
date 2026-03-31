def calculate_ingredient_amounts(ingredient_list, desired_servings):
    adjusted_list = []
    for ingredient in ingredient_list:
        name, amount = ingredient.split(':')
        amount_value = int(amount[:-2])
        unit = amount[-2:]
        adjusted_amount = amount_value * desired_servings
        adjusted_list.append(f"{name}:{adjusted_amount}{unit}")
    return adjusted_list