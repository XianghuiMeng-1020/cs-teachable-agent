def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile:
        recipes = infile.read().strip().split('\n\n')

    filtered_recipes = []

    for recipe in recipes:
        lines = recipe.strip().split('\n')
        recipe_name = lines[0].strip()
        ingredients = [line.strip() for line in lines[1:] if line.strip()]  # Filter out empty lines
        if len(ingredients) <= max_ingredients:
            filtered_recipes.append(recipe)

    with open(output_file, 'w') as outfile:
        outfile.write('\n\n'.join(filtered_recipes))
