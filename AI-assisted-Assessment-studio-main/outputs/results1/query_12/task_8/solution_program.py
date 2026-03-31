def can_cook_recipe(recipe, ingredients_file):
    with open(ingredients_file, 'r') as file:
        ingredient_data = file.readlines()
    available_ingredients = {}
    for line in ingredient_data:
        name, amount = line.strip().split(',')
        available_ingredients[name] = int(amount)
    for ingredient, required_amount in recipe.items():
        if ingredient not in available_ingredients or available_ingredients[ingredient] < required_amount:
            return False
    return True