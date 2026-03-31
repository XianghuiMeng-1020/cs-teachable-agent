def recipe_ingredients_calculator(file_path):
    ingredients_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            recipe = line.strip().split(':')
            if len(recipe) > 1:
                ingredients = recipe[1].split(',')
                ingredients_set.update(ingredients)
    return sorted(ingredients_set)