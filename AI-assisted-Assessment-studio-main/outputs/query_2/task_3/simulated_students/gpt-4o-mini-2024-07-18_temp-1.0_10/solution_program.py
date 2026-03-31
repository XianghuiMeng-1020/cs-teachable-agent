def format_recipe(file_input, file_output):
    with open(file_input, 'r') as infile, open(file_output, 'w') as outfile:
        for line in infile:
            title, ingredients, method = line.strip().split('--')
            ingredients_list = ingredients.split(', ')
            outfile.write(f'Recipe Title: {title}\n')
            outfile.write('Ingredients:\n')
            for ingredient in ingredients_list:
                outfile.write(f'- {ingredient}\n')
            outfile.write(f'Method:\n{method}\n\n')