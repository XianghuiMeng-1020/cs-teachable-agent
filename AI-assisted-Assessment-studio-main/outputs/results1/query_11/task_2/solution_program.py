def can_qualify(dish_ingredients, mandatory_ingredients):
    for ingredient in mandatory_ingredients:
        if ingredient not in dish_ingredients:
            return False
    return True
