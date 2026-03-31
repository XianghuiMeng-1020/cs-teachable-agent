def calculate_ingredient_amounts(ingredient_list, desired_servings):
    adjusted_ingredients = []
    for ingredient in ingredient_list:
        name, amount_with_unit = ingredient.split(':')
        amount = int(''.join(filter(str.isdigit, amount_with_unit)))
        unit = ''.join(filter(str.isalpha, amount_with_unit))
        total_amount = amount * desired_servings
        adjusted_ingredients.append(f"{name}:{total_amount}{unit}")
    return adjusted_ingredients