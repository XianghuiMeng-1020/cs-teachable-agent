def recipe_ingredients_calculator(file_path):
    ingredients = set()
    with open(file_path, 'r') as file:
        for line in file:
            _, ingredients_list = line.strip().split(':')
            ingredients.update(ingredients_list.split(','))
    return sorted(ingredients)