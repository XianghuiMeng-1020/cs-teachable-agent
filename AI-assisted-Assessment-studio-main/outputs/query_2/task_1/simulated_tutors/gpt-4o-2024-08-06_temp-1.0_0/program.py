def find_recipes_with_ingredient(file_path, ingredient):
    recipes_with_ingredient = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    current_recipe = None
    recipe_ingredients = []
    
    for line in lines:
        line = line.strip()  # Remove any leading/trailing whitespace
        
        if line == "":  # Blank line, signifies end of a recipe
            if ingredient in recipe_ingredients:
                recipes_with_ingredient.append(current_recipe)
            current_recipe = None
            recipe_ingredients = []  # Reset for the next recipe
        elif current_recipe is None:
            current_recipe = line  # The first line is the recipe name
        else:
            recipe_ingredients.append(line)  # Subsequent lines are ingredients
    
    # Check the last recipe in case the file does not end with a newline
    if ingredient in recipe_ingredients:
        recipes_with_ingredient.append(current_recipe)

    return recipes_with_ingredient