def can_qualify(dish_ingredients, mandatory_ingredients):
    # Check if all mandatory ingredients are in the dish ingredients
    for ingredient in mandatory_ingredients:
        if ingredient not in dish_ingredients:
            return False
    return True