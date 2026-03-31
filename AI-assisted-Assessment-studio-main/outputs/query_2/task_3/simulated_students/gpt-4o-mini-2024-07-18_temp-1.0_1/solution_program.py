def format_recipe(file_input, file_output):
    with open(file_input, 'r') as infile:
        recipes = infile.readlines()

    formatted_recipes = []
    for recipe in recipes:
        title, ingredients, method = recipe.strip().split('--')
        ingredients_list = ingredients.split(', ')
        formatted_recipe = f"Recipe Title: {title}\nIngredients:\n"
        formatted_recipe += '\n'.join([f'- {ingredient}' for ingredient in ingredients_list])
        formatted_recipe += f"\nMethod:\n{method}\n"
        formatted_recipes.append(formatted_recipe)

    with open(file_output, 'w') as outfile:
        outfile.write('\n\n'.join(formatted_recipes))