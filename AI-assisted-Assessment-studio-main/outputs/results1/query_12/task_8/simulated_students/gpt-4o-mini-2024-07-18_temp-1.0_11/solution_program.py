def can_cook_recipe(recipe, ingredients_file):
    available_ingredients = {}
    with open(ingredients_file, 'r') as file:
        for line in file:
            name, amount = line.strip().split(',')
            available_ingredients[name] = int(amount)

    for ingredient, amount_needed in recipe.items():
        if available_ingredients.get(ingredient, 0) < amount_needed:
            return False
    return True