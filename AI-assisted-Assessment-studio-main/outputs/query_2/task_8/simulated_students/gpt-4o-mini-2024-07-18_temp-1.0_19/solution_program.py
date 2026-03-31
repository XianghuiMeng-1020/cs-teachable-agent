def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        recipe_lines = infile.readlines()
        current_recipe = []
        ingredient_count = 0

        for line in recipe_lines:
            if line.strip() == '':
                if ingredient_count <= max_ingredients:
                    outfile.write(''.join(current_recipe) + '\n')
                current_recipe = []
                ingredient_count = 0
            else:
                if ingredient_count == 0:
                    current_recipe.append(line)  # Append recipe name
                current_recipe.append(line)
                ingredient_count += 1

        # Check the last recipe if the file does not end with a blank line
        if ingredient_count <= max_ingredients:
            outfile.write(''.join(current_recipe) + '\n')