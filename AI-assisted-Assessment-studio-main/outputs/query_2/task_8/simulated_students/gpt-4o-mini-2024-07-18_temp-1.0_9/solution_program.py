def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        recipe = []
        for line in infile:
            line = line.strip()
            if line == '':
                if recipe:
                    recipe_name = recipe[0]
                    ingredients = recipe[1:]
                    if len(ingredients) <= max_ingredients:
                        outfile.write(recipe_name + '\n')
                        for ingredient in ingredients:
                            outfile.write(ingredient + '\n')
                        outfile.write('\n')
                    recipe = []
            else:
                recipe.append(line)
        # Handle the last recipe if the file does not end with a new line
        if recipe:
            recipe_name = recipe[0]
            ingredients = recipe[1:]
            if len(ingredients) <= max_ingredients:
                outfile.write(recipe_name + '\n')
                for ingredient in ingredients:
                    outfile.write(ingredient + '\n')
