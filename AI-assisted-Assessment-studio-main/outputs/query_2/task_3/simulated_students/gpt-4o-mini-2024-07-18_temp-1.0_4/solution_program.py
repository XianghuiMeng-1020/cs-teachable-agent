def format_recipe(file_input, file_output):
    with open(file_input, 'r') as infile, open(file_output, 'w') as outfile:
        for line in infile:
            title, ingredients, method = line.strip().split('--')
            ingredients_list = ingredients.split(', ')
            formatted_recipe = f'Recipe Title: {title}\nIngredients:\n'
            for ingredient in ingredients_list:
                formatted_recipe += f'- {ingredient}\n'
            formatted_recipe += f'Method:\n{method}\n\n'
            outfile.write(formatted_recipe)