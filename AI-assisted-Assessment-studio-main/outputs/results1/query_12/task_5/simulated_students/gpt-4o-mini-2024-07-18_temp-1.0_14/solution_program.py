def recipe_manager(filename):
    recipes = []
    with open(filename, 'r') as file:
        recipe = ''
        for line in file:
            if line.strip():
                recipe += line
            else:
                if recipe:
                    recipes.append(recipe.strip())
                    recipe = ''
        if recipe:
            recipes.append(recipe.strip())

    for recipe in recipes:
        print(recipe)
        print()  # For spacing between recipes

    while True:
        ingredient = input('Enter an ingredient to search (or type "EXIT" to quit): ')
        if ingredient == "EXIT":
            break
        found_recipes = []
        for recipe in recipes:
            if f'Ingredients: ' in recipe:
                parts = recipe.split('Ingredients: ')[1].split('\n')[0]
                ingredients = [i.strip() for i in parts.split(',')]
                if ingredient in ingredients:
                    recipe_name = recipe.split('\n')[0]
                    found_recipes.append(recipe_name)
        if found_recipes:
            print(f'The ingredient "{ingredient}" is used in the following recipes: {', '.join(found_recipes)}')
        else:
            print(f'The ingredient "{ingredient}" is not found in any recipes.')