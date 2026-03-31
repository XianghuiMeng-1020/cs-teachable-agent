def recipe_ingredients_calculator(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    ingredients = set()
    for line in content:
        if ':' in line:
            name, ingr = line.split(':', 1)
            ingredient_list = [x.strip() for x in ingr.split(',')]
            ingredients.update(ingredient_list)
    return sorted(ingredients)