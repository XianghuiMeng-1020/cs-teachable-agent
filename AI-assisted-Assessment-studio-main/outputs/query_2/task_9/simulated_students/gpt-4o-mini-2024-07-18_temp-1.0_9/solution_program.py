def recipe_ingredients_calculator(file_path):
    ingredients_set = set()
    with open(file_path, 'r') as file:
        for line in file:
            recipe = line.strip()  # Remove any extra whitespace
            if ':' in recipe:
                _, ingredients = recipe.split(':', 1)  # Split on the first colon
                ingredients_list = ingredients.split(',')  # Split ingredients by comma
                ingredients_set.update(ingredient.strip() for ingredient in ingredients_list)  # Add to set
    return sorted(ingredients_set)  # Return sorted list of unique ingredients