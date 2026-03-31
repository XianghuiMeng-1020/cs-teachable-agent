def recipe_ingredients_calculator(file_path):
    ingredients = set()
    with open(file_path, 'r') as file:
        for line in file:
            _, ingredient_list = line.split(':')
            ingredients.update(ingredient.strip() for ingredient in ingredient_list.split(','))
    return sorted(ingredients)