def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    filtered_recipes = []
    current_recipe = []
    ingredient_count = 0
    recipe_started = False

    for line in lines:
        line = line.strip()  # Remove any extra newline characters
        if line == '':
            # End of current recipe
            if recipe_started and ingredient_count <= max_ingredients:
                filtered_recipes.extend(current_recipe)
                filtered_recipes.append('')  # Add back the newline
            current_recipe = []
            ingredient_count = 0
            recipe_started = False
        elif not recipe_started:
            # Start of a new recipe
            current_recipe.append(line)
            recipe_started = True
        else:
            # Add ingredient to the current recipe
            current_recipe.append(line)
            ingredient_count += 1

    with open(output_file, 'w') as f:
        for recipe_line in filtered_recipes:
            if recipe_line == '':
                f.write('\n')
            else:
                f.write(f"{recipe_line}\n")