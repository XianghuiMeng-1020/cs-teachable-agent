def format_recipe(file_input, file_output):
    with open(file_input, 'r') as f:
        recipes = f.readlines()
    formatted_recipes = []
    for recipe in recipes:
        title, ingredients, method = recipe.split('--')
        ingredient_list = ingredients.split(', ')
        ingredients_string = '\n'.join(['- ' + ingredient for ingredient in ingredient_list])
        formatted_recipe = (f"Recipe Title: {title.strip()}\n" 
                            f"Ingredients:\n"
                            f"{ingredients_string}\n"
                            f"Method:\n{method.strip()}\n\n")
        formatted_recipes.append(formatted_recipe)
    with open(file_output, 'w') as f:
        f.writelines(formatted_recipes)