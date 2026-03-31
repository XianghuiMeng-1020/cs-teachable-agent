def recipe_ingredients_calculator(file_path):
    ingredients_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            recipe = line.strip().split(':')[1]
            ingredients = recipe.split(',')
            ingredients_set.update(ingredient.strip() for ingredient in ingredients)
    return sorted(ingredients_set)