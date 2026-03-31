def filter_ingredients(input_file, output_file, max_ingredients):
    with open(input_file, 'r') as infile:
        lines = infile.read().split('\n')

    current_recipe = []
    recipes_to_write = []

    for line in lines:
        if line == '':
            if len(current_recipe[1:]) <= max_ingredients:
                recipes_to_write.extend(current_recipe)
                recipes_to_write.append('')
            current_recipe = []
        else:
            current_recipe.append(line)

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(recipes_to_write))