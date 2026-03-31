def recipe_manager(filename):
    recipes = []
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n\n')
        for recipe in content:
            if recipe:
                lines = recipe.strip().split('\n')
                recipe_name = lines[0].strip()
                ingredient_line = lines[1].strip() if len(lines) > 1 else ''
                ingredients = ingredient_line.replace('Ingredients: ', '').split(', ') if ingredient_line else []
                recipes.append((recipe_name, ingredients))

    for recipe_name, ingredients in recipes:
        print(recipe_name)
        print('Ingredients:', ', '.join(ingredients))
        print('Steps:')
        steps_start = 2
        for i in range(steps_start, len(lines)):
            print(lines[i])
        print() 

    while True:
        ingredient_query = input('Enter ingredient to check (or type EXIT to quit): ').strip()
        if ingredient_query == 'EXIT':
            break
        found_recipes = [recipe_name for recipe_name, ingredients in recipes if ingredient_query in ingredients]
        if found_recipes:
            print(f'Ingredient "{ingredient_query}" found in recipes: {', '.join(found_recipes)}')
        else:
            print(f'Ingredient "{ingredient_query}" not found in any recipe.')