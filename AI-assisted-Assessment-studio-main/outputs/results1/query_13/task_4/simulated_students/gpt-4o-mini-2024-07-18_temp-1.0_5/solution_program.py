def calculate_total_ingredients(ingredient_list):
    ingredients_dict = {}
    for item in ingredient_list:
        try:
            ingredient, quantity = item.split(':')
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError('Quantity must be a positive integer')
            if ingredient in ingredients_dict:
                ingredients_dict[ingredient] += quantity
            else:
                ingredients_dict[ingredient] = quantity
        except (ValueError, IndexError):
            continue
    return ingredients_dict