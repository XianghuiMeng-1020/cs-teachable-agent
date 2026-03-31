def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile:
        recipes = infile.read().strip().split('\n\n')

    filtered_recipes = []
    for recipe in recipes:
        lines = recipe.strip().split('\n')
        if len(lines) > 0:
            recipe_name = lines[0]
            ingredients = lines[1:]  # All lines after the recipe name are considered ingredients
            if len(ingredients) <= max_ingredients:
                filtered_recipes.append(recipe)

    with open(output_file, 'w') as outfile:
        outfile.write('\n\n'.join(filtered_recipes))