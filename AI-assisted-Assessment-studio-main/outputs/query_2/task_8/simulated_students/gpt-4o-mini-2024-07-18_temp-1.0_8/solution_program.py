def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        recipe_name = None
        ingredients = []
        for line in infile:
            line = line.strip()
            if line == '':
                if recipe_name is not None:
                    if len(ingredients) <= max_ingredients:
                        outfile.write(f'{recipe_name}\n')
                        for ingredient in ingredients:
                            outfile.write(f'{ingredient}\n')
                        outfile.write('\n')
                recipe_name = None
                ingredients = []
            elif recipe_name is None:
                recipe_name = line
            else:
                ingredients.append(line)
        if recipe_name is not None:
            if len(ingredients) <= max_ingredients:
                outfile.write(f'{recipe_name}\n')
                for ingredient in ingredients:
                    outfile.write(f'{ingredient}\n')
                outfile.write('\n')