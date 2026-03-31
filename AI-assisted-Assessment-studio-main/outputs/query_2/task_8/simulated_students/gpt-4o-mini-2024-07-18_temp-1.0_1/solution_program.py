def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    recipes = []
    current_recipe = []

    for line in lines:
        line = line.strip()
        if line == '':  # end of a recipe
            if current_recipe:
                recipes.append(current_recipe)
                current_recipe = []
        else:
            current_recipe.append(line)

    if current_recipe:  # in case the last recipe has no following blank line
        recipes.append(current_recipe)

    filtered_recipes = []
    for recipe in recipes:
        name = recipe[0]  # first line is the recipe name
        ingredients = recipe[1:]  # rest are ingredients
        if len(ingredients) <= max_ingredients:
            filtered_recipes.append(recipe)

    with open(output_file, 'w') as outfile:
        for recipe in filtered_recipes:
            outfile.write(recipe[0] + '\n')  # write recipe name
            for ingredient in recipe[1:]:
                outfile.write(ingredient + '\n')  # write each ingredient
            outfile.write('\n')  # blank line after each recipe