def recipe_ingredients_calculator(file_path):
    ingredients = set()
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by ':' and take the part after the colon
            recipe_info = line.split(':')
            if len(recipe_info) > 1:
                # Get the ingredients and split them by ','
                recipe_ingredients = recipe_info[1].strip().split(',')
                ingredients.update([ingredient.strip() for ingredient in recipe_ingredients])
    # Sort the unique ingredients
    return sorted(ingredients)