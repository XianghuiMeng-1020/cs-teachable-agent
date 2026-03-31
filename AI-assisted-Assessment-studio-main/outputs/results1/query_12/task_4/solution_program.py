def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as f:
        recipes = f.read().strip().split('\n\n')
    recipe_tuples = []
    for recipe in recipes:
        lines = recipe.split('\n')
        recipe_tuples.append((lines[0], recipe))
    recipe_tuples.sort()
    with open(output_file, 'w') as f:
        for _, recipe in recipe_tuples:
            f.write(recipe + '\n\n')