def calculate_ingredient_amounts(ingredient_list, desired_servings):
    result = []
    for item in ingredient_list:
        ingredient, amount_with_unit = item.split(':')
        amount_str = ''.join(filter(str.isdigit, amount_with_unit))
        unit = ''.join(filter(str.isalpha, amount_with_unit))
        amount = int(amount_str) * desired_servings
        result.append(f"{ingredient}:{amount}{unit}")
    return result