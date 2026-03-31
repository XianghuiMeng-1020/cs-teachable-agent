def recipe_ingredients_calculator(file_path):
    ingredients = set()
    with open(file_path, 'r') as file:
        for line in file:
            _, ing_list = line.split(':')
            ingredients.update(ing_list.split(','))
    return sorted(ingredients)