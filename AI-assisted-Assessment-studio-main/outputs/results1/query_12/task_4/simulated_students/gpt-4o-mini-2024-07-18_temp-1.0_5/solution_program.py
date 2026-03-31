def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as infile:
        content = infile.read().strip().split('\n\n')

    recipes = []
    for recipe in content:
        lines = recipe.strip().split('\n')
        if lines:
            recipe_name = lines[0]
            ingredients = lines[1:]  # All lines after the first line are ingredients
            recipes.append((recipe_name, ingredients))

    recipes.sort()  # Sort by recipe name

    with open(output_file, 'w') as outfile:
        for recipe_name, ingredients in recipes:
            outfile.write(recipe_name + '\n')
            outfile.write('\n'.join(ingredients) + '\n\n')