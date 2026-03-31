def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as infile:
        content = infile.read().strip()
    recipes = content.split('\n\n')  # Split by double new lines to separate recipes

    recipe_list = []
    for recipe in recipes:
        lines = recipe.strip().split('\n')  # Split by new lines to get recipe name and ingredients
        if lines:
            recipe_name = lines[0].strip()
            ingredients = lines[1:]  # Remaining lines are ingredients
            recipe_list.append((recipe_name, ingredients))

    # Sort recipes by name
    recipe_list.sort(key=lambda x: x[0])

    # Write sorted recipes to output file
    with open(output_file, 'w') as outfile:
        for recipe_name, ingredients in recipe_list:
            outfile.write(recipe_name + '\n')
            outfile.write('\n'.join(ingredients) + '\n\n')