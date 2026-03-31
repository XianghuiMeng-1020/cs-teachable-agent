def calculate_ingredient_amounts(ingredient_list, desired_servings):
    adjusted_ingredients = []
    for ingredient in ingredient_list:
        name, amount = ingredient.split(':')
        numeric_amount = int(amount[:-2])
        unit = amount[-2:]
        total_amount = numeric_amount * desired_servings
        adjusted_ingredients.append(f"{name}:{total_amount}{unit}")
    return adjusted_ingredients