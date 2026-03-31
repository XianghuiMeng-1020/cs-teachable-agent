def can_cook_recipe(recipe, ingredients_file):
    available_ingredients = {}
    with open(ingredients_file, 'r') as file:
        for line in file:
            ingredient, amount = line.strip().split(',')
            available_ingredients[ingredient] = int(amount)

    for ingredient, needed_amount in recipe.items():
        if ingredient not in available_ingredients or available_ingredients[ingredient] < needed_amount:
            return False
    return True