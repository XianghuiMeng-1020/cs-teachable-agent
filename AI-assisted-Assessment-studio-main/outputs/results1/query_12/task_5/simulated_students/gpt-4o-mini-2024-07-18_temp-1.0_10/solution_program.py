def recipe_manager(filename):
    with open(filename, 'r') as file:
        content = file.read()

    recipes = content.split('\n\n')
    recipe_list = []

    for recipe in recipes:
        if recipe.strip():
            recipe_list.append(recipe.strip())
            print(recipe.strip())

    while True:
        ingredient_query = input('Enter an ingredient to search (or type EXIT to quit): ')
        if ingredient_query == 'EXIT':
            break
        found_recipes = []
        for recipe in recipe_list:
            lines = recipe.split('\n')
            ingredients_line = lines[1]  # Ingredients line
            ingredients = ingredients_line[len('Ingredients: '):].split(', ')
            if ingredient_query in ingredients:
                recipe_name = lines[0]
                found_recipes.append(recipe_name)
        if found_recipes:
            print(f'The ingredient {ingredient_query} is used in: {', '.join(found_recipes)}')
        else:
            print(f'The ingredient {ingredient_query} is not found.')