def check_ingredient_availability(ingredients, required_item, required_quantity):
    ingredient_dict = {}
    for ingredient in ingredients:
        name, quantity = ingredient.rsplit(' ', 1)
        ingredient_dict[name] = int(quantity)
    if required_item in ingredient_dict:
        if ingredient_dict[required_item] >= required_quantity:
            return 'Available'
    return 'Not Available'