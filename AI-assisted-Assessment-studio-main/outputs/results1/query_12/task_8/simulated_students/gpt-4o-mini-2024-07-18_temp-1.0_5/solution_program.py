def can_cook_recipe(recipe, ingredients_file):
    ingredients = {}
    with open(ingredients_file, 'r') as file:
        for line in file:
            name, amount = line.strip().split(',')
            ingredients[name] = int(amount)

    for ingredient, needed in recipe.items():
        if ingredients.get(ingredient, 0) < needed:
            return False

    return True