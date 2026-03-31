def can_cook_recipe(recipe, ingredients_file):
    ingredients = {}
    with open(ingredients_file, 'r') as file:
        for line in file:
            name, amount = line.strip().split(',')
            ingredients[name] = int(amount)

    for ingredient, required_amount in recipe.items():
        if ingredient not in ingredients or ingredients[ingredient] < required_amount:
            return False

    return True