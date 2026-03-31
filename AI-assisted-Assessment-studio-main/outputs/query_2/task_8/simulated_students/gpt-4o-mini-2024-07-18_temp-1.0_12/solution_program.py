def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile:
        recipes = infile.read().strip().split('\n\n')

    with open(output_file, 'w') as outfile:
        for recipe in recipes:
            lines = recipe.strip().split('\n')
            recipe_name = lines[0]
            ingredients = lines[1:]  
            if len(ingredients) <= max_ingredients:
                outfile.write(recipe + '\n\n')