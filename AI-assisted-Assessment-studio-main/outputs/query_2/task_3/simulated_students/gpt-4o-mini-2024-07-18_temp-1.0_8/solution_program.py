def format_recipe(file_input, file_output):
    with open(file_input, 'r') as infile, open(file_output, 'w') as outfile:
        recipes = infile.readlines()
        formatted_recipes = []
        for recipe in recipes:
            title, ingredients, method = recipe.strip().split('--')
            formatted_recipe = f'Recipe Title: {title}\nIngredients:\n' + 
            '\n'.join([f'- {ingredient.strip()}' for ingredient in ingredients.split(',')]) + 
            f'\nMethod:\n{method.strip()}'
            formatted_recipes.append(formatted_recipe)
        outfile.write('\n\n'.join(formatted_recipes))