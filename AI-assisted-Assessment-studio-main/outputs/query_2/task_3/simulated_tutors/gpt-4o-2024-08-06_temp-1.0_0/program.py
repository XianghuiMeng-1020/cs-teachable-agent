def format_recipe(file_input, file_output):
    with open(file_input, 'r') as file_in:
        lines = file_in.readlines()

    formatted_recipes = []
    for line in lines:
        line = line.strip()
        if line:  # Ignore empty lines
            parts = line.split('--')
            if len(parts) == 3:
                title, ingredients, method = parts

                # Split ingredients and format them
                ingredients_list = ingredients.split(', ')
                formatted_ingredients = '\n'.join(['- ' + ing for ing in ingredients_list])

                # Format the recipe
                formatted_recipe = f"Recipe Title: {title}\nIngredients:\n{formatted_ingredients}\nMethod:\n{method}\n"

                formatted_recipes.append(formatted_recipe)

    with open(file_output, 'w') as file_out:
        file_out.write('\n\n'.join(formatted_recipes) + '\n')