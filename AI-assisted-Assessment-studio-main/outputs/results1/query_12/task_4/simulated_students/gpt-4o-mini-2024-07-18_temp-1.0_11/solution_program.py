def sort_recipes(input_file, output_file):
    with open(input_file, 'r') as infile:
        # Read the contents of the input file
        content = infile.read().strip()

    # Split recipes by double newlines (empty lines)
    recipes = content.split('\n\n')

    # Prepare a list to store formatted recipes
    recipe_list = []

    for recipe in recipes:
        # Split each recipe into lines
        recipe_lines = recipe.strip().split('\n')
        # Extract recipe name and ingredients along with their quantities
        recipe_name = recipe_lines[0]
        ingredients = recipe_lines[1:]  # The rest are ingredients and quantities
        recipe_list.append((recipe_name, ingredients))

    # Sort the recipes list based on the recipe name (first element of the tuple)
    sorted_recipes = sorted(recipe_list, key=lambda x: x[0])

    # Prepare the output content
    output_content = []
    for recipe_name, ingredients in sorted_recipes:
        output_content.append(recipe_name)
        output_content.extend(ingredients)
        output_content.append('')  # Adding an empty line after each recipe

    # Write the sorted recipes to the output file
    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(output_content).strip())