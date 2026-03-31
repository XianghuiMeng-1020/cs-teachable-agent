def recipe_ingredients_calculator(file_path):
    unique_ingredients = set()
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                ingredients_part = line.split(':')[1]
                ingredients = ingredients_part.split(',')
                unique_ingredients.update(ingredient.strip() for ingredient in ingredients)
    return sorted(unique_ingredients)