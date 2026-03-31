def recipe_manager(filename):
    with open(filename, 'r') as file:
        content = file.read()

    recipes = content.strip().split('\n\n')
    recipe_list = []
    ingredient_map = {}

    for recipe in recipes:
        lines = recipe.strip().split('\n')
        recipe_name = lines[0]
        ingredients_line = lines[1] if len(lines) > 1 else ''
        steps = lines[2:] if len(lines) > 2 else []

        recipe_list.append(recipe_name)
        ingredients = ingredients_line.split(': ')[1].split(', ') if ':' in ingredients_line else []

        for ingredient in ingredients:
            if ingredient not in ingredient_map:
                ingredient_map[ingredient] = []
            ingredient_map[ingredient].append(recipe_name)

    for recipe in recipe_list:
        print(recipe)

    while True:
        user_input = input('Enter an ingredient to search (or type EXIT to quit): ')
        if user_input == 'EXIT':
            break
        if user_input in ingredient_map:
            print(f'Recipes containing {user_input}: {", ".join(ingredient_map[user_input])}')
        else:
            print(f'The ingredient {user_input} is not found in any recipe.')