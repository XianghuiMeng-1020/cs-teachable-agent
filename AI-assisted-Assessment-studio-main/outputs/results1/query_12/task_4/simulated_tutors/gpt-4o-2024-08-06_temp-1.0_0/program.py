def sort_recipes(input_file, output_file):
    try:
        with open(input_file, 'r') as in_file:
            recipes = in_file.read().strip().split('\n\n')

        # Parse recipes into a list of tuples (recipe_name, full_recipe_string)
        parsed_recipes = []
        for recipe in recipes:
            if recipe.strip():
                lines = recipe.strip().split('\n')
                recipe_name = lines[0]
                parsed_recipes.append((recipe_name, recipe))

        # Sort recipes by their names
        parsed_recipes.sort(key=lambda x: x[0])

        # Write sorted recipes to output file
        with open(output_file, 'w') as out_file:
            for _, full_recipe_string in parsed_recipes:
                out_file.write(full_recipe_string + '\n\n')
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"An error occurred: {e}")