def recipe_ingredients_calculator(file_path):
    ingredients_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            recipe, ingredients = line.split(':')
            ingredients_list = ingredients.strip().split(',')
            ingredients_set.update(ingredients_list)
    sorted_ingredients = sorted(ingredients_set)
    return sorted_ingredients