def recipe_manager(filename):
    recipes = []
    with open(filename, 'r') as file:
        recipe = ''
        for line in file:
            if line.strip() == '':
                if recipe:
                    recipes.append(recipe.strip())
                    recipe = ''
                continue
            recipe += line
        if recipe:
            recipes.append(recipe.strip())

    for recipe in recipes:
        print(recipe)

    while True:
        ingredient = input('Enter an ingredient to search (or type EXIT to quit): ')
        if ingredient == 'EXIT':
            break
        found_recipes = []
        for recipe in recipes:
            if f'Ingredients: ' in recipe:
                ingredients_section = recipe.split('Ingredients: ')[1].split('\nSteps:')[0]
                ingredients = [i.strip() for i in ingredients_section.split(',')]
                if ingredient in ingredients:
                    found_recipes.append(recipe.split('\n')[0])
        if found_recipes:
            print(f'The ingredient "{ingredient}" is used in the following recipes:')
            for r in found_recipes:
                print(f'- {r}')
        else:
            print(f'The ingredient "{ingredient}" is not found in any recipe.')