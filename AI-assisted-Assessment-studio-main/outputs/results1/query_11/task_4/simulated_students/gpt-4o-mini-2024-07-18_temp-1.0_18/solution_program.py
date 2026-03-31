def calculate_ingredient_amounts(ingredient_list, desired_servings):
    adjusted_ingredients = []
    for ingredient in ingredient_list:
        name, amount = ingredient.split(':')
        amount_value = int(''.join(filter(str.isdigit, amount)))
        amount_unit = ''.join(filter(str.isalpha, amount))
        total_amount = amount_value * desired_servings
        adjusted_ingredients.append(f"{name}:{total_amount}{amount_unit}")
    return adjusted_ingredients