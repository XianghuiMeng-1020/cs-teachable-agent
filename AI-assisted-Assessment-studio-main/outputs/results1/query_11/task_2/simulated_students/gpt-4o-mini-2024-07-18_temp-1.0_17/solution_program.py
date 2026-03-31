def can_qualify(dish_ingredients, mandatory_ingredients):
    return all(ingredient in dish_ingredients for ingredient in mandatory_ingredients)