def recipe_ingredients_calculator(file_path):
    ingredients = set()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) > 1:
                recipe_ingredients = parts[1].split(',')
                ingredients.update(ingredient.strip() for ingredient in recipe_ingredients)
    return sorted(ingredients)