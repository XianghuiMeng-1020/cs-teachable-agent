def recipe_ingredients_calculator(file_path):
    ingredients_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                ingredients = line.split(':')[1].strip().split(',')
                ingredients_set.update(ingredient.strip() for ingredient in ingredients)
    return sorted(ingredients_set)