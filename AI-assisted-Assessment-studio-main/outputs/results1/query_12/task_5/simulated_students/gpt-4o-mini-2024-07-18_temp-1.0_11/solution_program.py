def recipe_manager(filename):
    with open(filename, 'r') as file:
        content = file.read()

    recipes = content.strip().split('\n\n')
    recipe_list = []
    ingredient_map = {}

    for recipe in recipes:
        lines = recipe.split('\n')
        recipe_name = lines[0].strip()
        ingredients_line = lines[1].strip()
        ingredients = ingredients_line.replace('Ingredients: ', '').split(', ')
        recipe_list.append(recipe_name)
        for ingredient in ingredients:
            if ingredient not in ingredient_map:
                ingredient_map[ingredient] = []
            ingredient_map[ingredient].append(recipe_name)

    for recipe in recipe_list:
        print(recipe)

    while True:
        user_input = input('Enter an ingredient to search for (or type EXIT to quit): ').strip()
        if user_input == 'EXIT':
            break
        if user_input in ingredient_map:
            print(f'The ingredient "{user_input}" is found in recipes: {', '.join(ingredient_map[user_input])}')
        else:
            print(f'The ingredient "{user_input}" is not found in any recipe.')