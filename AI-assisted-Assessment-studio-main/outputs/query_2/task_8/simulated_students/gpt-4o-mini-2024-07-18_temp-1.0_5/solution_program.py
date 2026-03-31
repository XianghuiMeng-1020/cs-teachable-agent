def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        recipe_lines = infile.readlines()
        current_recipe = []
        ingredient_count = 0

        for line in recipe_lines:
            line = line.strip()
            if line:
                # If line is not empty, we are either reading a recipe name or ingredients
                if ingredient_count == 0:
                    # First line after empty line is the name of the recipe
                    current_recipe.append(line)
                else:
                    # Subsequent lines are ingredients
                    current_recipe.append(line)
                ingredient_count += 1
            else:
                # We hit an empty line, meaning the end of the current recipe
                if ingredient_count > 0:
                    # Write the recipe to the output file if it has valid ingredient count
                    if ingredient_count <= max_ingredients:
                        outfile.write('\n'.join(current_recipe) + '\n\n')
                # Reset for the next recipe
                current_recipe = []
                ingredient_count = 0

        # Check the last recipe after the loop
        if ingredient_count > 0:
            if ingredient_count <= max_ingredients:
                outfile.write('\n'.join(current_recipe) + '\n')