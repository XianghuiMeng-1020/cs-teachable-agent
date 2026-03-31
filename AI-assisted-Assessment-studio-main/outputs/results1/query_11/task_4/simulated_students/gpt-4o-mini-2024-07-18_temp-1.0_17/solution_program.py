def calculate_ingredient_amounts(ingredient_list, desired_servings):
    adjusted_ingredients = []
    for ingredient in ingredient_list:
        name, amount = ingredient.split(':')
        quantity, unit = ''.join(filter(str.isdigit, amount)), ''.join(filter(str.isalpha, amount))
        new_amount = int(quantity) * desired_servings
        adjusted_ingredients.append(f'{name}:{new_amount}{unit}')
    return adjusted_ingredients