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
                    filtered_recipes.append(recipe_name + '\n' + '\n'.join(ingredients) + '\n')
            recipe_name = None
            ingredients = []
        elif recipe_name is None:
            recipe_name = line
        else:
            ingredients.append(line)

    if recipe_name is not None and len(ingredients) <= max_ingredients:
        filtered_recipes.append(recipe_name + '\n' + '\n'.join(ingredients) + '\n')

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(filtered_recipes))