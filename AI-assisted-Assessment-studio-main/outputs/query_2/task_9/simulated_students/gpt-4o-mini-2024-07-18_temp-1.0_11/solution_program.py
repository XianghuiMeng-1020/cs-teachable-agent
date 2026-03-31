def recipe_ingredients_calculator(file_path):
    ingredients_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            recipe = line.strip().split(':')
            if len(recipe) > 1:
                ingredients = recipe[1].split(',')
                ingredients_set.update(ingredient.strip() for ingredient in ingredients)
    sorted_ingredients = sorted(ingredients_set)
    return sorted_ingredients