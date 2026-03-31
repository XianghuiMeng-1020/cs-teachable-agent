def recipe_ingredients_calculator(file_path):
    ingredients = set()
    with open(file_path, 'r') as file:
        for line in file:
            recipe = line.split(':')[1].strip()
            ingredient_list = recipe.split(',')
            ingredients.update(map(str.strip, ingredient_list))
    return sorted(ingredients)