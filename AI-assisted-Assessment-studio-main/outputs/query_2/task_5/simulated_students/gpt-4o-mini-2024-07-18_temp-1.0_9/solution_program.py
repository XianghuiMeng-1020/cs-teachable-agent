def sort_ingredients(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        recipes = infile.readlines()

    sorted_recipes = []
    for recipe in recipes:
        ingredients = recipe.strip().split(',')
        sorted_ingredients = sorted(ingredient.strip() for ingredient in ingredients)
        sorted_recipes.append(', '.join(sorted_ingredients))

    with open(output_filename, 'w') as outfile:
        outfile.write('\n'.join(sorted_recipes) + '\n')