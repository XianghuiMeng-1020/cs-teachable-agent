def format_recipe(file_input, file_output):
    with open(file_input, 'r') as infile:
        recipes = infile.readlines()

    with open(file_output, 'w') as outfile:
        for recipe in recipes:
            title, ingredients, method = recipe.strip().split('--')
            formatted_recipe = f"Recipe Title: {title}\nIngredients:\n"
            formatted_recipe += '\n'.join([f'- {ingredient.strip()}' for ingredient in ingredients.split(',')]) + '\n'
            formatted_recipe += f"Method:\n{method.strip()}\n\n"
            outfile.write(formatted_recipe)