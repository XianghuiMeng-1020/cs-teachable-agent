def format_recipe(file_input, file_output):
    with open(file_input, 'r') as f:
        recipes = f.readlines()
    formatted_recipes = []
    for recipe in recipes:
        title, ingredients, method = recipe.strip().split('--')
        ingredient_list = ingredients.split(', ')
        formatted_recipe = f'Recipe Title: {title}\nIngredients:'
        for ingredient in ingredient_list:
            formatted_recipe += f'\n- {ingredient}'
        formatted_recipe += f'\nMethod:\n{method}'
        formatted_recipes.append(formatted_recipe)
    with open(file_output, 'w') as f:
        f.write('\n\n'.join(formatted_recipes))