def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    filtered_recipes = []
    recipe_name = None
    ingredients = []

    for line in lines:
        line = line.strip()
        if line == '':
            if recipe_name is not None:
                if len(ingredients) <= max_ingredients:
                    filtered_recipes.append(recipe_name)
                    filtered_recipes.extend(ingredients)
                    filtered_recipes.append('')  # add an empty line for separation
            recipe_name = None
            ingredients = []
        elif recipe_name is None:
            recipe_name = line
        else:
            ingredients.append(line)

    # Handle the last recipe if there's no trailing newline
    if recipe_name is not None:
        if len(ingredients) <= max_ingredients:
            filtered_recipes.append(recipe_name)
            filtered_recipes.extend(ingredients)

    with open(output_file, 'w') as outfile:
        for recipe in filtered_recipes:
            outfile.write(recipe + '\n')