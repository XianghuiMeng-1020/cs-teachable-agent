def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile:
        recipes = infile.read().strip().split('\n\n')
 
    filtered_recipes = []
    for recipe in recipes:
        lines = recipe.strip().split('\n')
        recipe_name = lines[0]
        ingredients = lines[1:]  # All lines except the first one are ingredients
        if len(ingredients) <= max_ingredients:
            filtered_recipes.append(recipe)
 
    with open(output_file, 'w') as outfile:
        for recipe in filtered_recipes:
            outfile.write(recipe + '\n\n')