def recipe_ingredients_calculator(file_path):
    unique_ingredients = set()
    with open(file_path, 'r') as file:
        for line in file:
            recipe = line.strip().split(':')
            if len(recipe) > 1:
                ingredients = recipe[1].split(',')
                unique_ingredients.update(ingredient.strip() for ingredient in ingredients)
    return sorted(unique_ingredients)