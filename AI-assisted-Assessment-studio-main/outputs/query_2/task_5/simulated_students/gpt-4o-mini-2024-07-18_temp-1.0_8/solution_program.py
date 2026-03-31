def sort_ingredients(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        recipes = infile.readlines()
    sorted_recipes = []
    for recipe in recipes:
        ingredients = [ingredient.strip() for ingredient in recipe.split(',')]
        ingredients.sort()
        sorted_recipes.append(', '.join(ingredients))
    with open(output_filename, 'w') as outfile:
        for sorted_recipe in sorted_recipes:
            outfile.write(sorted_recipe + '\n')