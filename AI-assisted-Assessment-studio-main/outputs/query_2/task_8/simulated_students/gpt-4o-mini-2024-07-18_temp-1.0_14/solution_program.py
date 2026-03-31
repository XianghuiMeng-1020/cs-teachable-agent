def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        recipe_lines = infile.readlines()
        i = 0
        while i < len(recipe_lines):
            recipe_name = recipe_lines[i].strip()
            i += 1
            ingredients = []
            while i < len(recipe_lines) and recipe_lines[i].strip() != '':
                ingredients.append(recipe_lines[i].strip())
                i += 1
            i += 1  # To skip the empty line
            if len(ingredients) <= max_ingredients:
                outfile.write(recipe_name + '\n')
                for ingredient in ingredients:
                    outfile.write(ingredient + '\n')
                outfile.write('\n')