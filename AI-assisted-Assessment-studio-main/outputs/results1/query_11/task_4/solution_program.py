def calculate_ingredient_amounts(ingredient_list, desired_servings):
    adjusted_ingredients = []
    for item in ingredient_list:
        ingredient, amount = item.split(':')
        number = int(amount[:-2])
        unit = amount[-2:]
        adjusted_amount = number * desired_servings
        adjusted_ingredient = f"{ingredient}:{adjusted_amount}{unit}"
        adjusted_ingredients.append(adjusted_ingredient)
    return adjusted_ingredients