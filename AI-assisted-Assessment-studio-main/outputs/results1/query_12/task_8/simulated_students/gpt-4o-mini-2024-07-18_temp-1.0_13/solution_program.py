def can_cook_recipe(recipe, ingredients_file):
    available_ingredients = {}
    with open(ingredients_file, 'r') as file:
        for line in file:
            ingredient, amount = line.strip().split(',')
            available_ingredients[ingredient] = int(amount)

    for ingredient, required_amount in recipe.items():
        if available_ingredients.get(ingredient, 0) < required_amount:
            return False

    return True