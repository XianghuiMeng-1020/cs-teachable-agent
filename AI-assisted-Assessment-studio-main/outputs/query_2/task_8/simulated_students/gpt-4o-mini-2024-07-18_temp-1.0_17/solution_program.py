def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        recipe_name = ''
        ingredients = []
        for line in infile:
            line = line.strip()
            if line == '':
                if recipe_name and len(ingredients) <= max_ingredients:
                    outfile.write(recipe_name + '\n')
                    for ingredient in ingredients:
                        outfile.write(ingredient + '\n')
                    outfile.write('\n')
                recipe_name = ''
                ingredients = []
            elif not recipe_name:
                recipe_name = line
            else:
                ingredients.append(line)
        if recipe_name and len(ingredients) <= max_ingredients:
            outfile.write(recipe_name + '\n')
            for ingredient in ingredients:
                outfile.write(ingredient + '\n')
            outfile.write('\n')