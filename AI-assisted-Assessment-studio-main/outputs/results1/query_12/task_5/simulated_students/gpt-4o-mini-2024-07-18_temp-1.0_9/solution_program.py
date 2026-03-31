def recipe_manager(filename):
    with open(filename, 'r') as file:
        recipes = []
        current_recipe = {}
        lines = file.readlines()
        for line in lines:
            stripped_line = line.strip()
            if stripped_line == '':
                if current_recipe:
                    recipes.append(current_recipe)
                    current_recipe = {}
                continue
            if 'Ingredients:' in stripped_line:
                current_recipe['Ingredients'] = stripped_line.split(': ')[1].split(', ')
            elif 'Steps:' in stripped_line:
                current_recipe['Steps'] = []
            elif current_recipe.get('Steps') is not None:
                current_recipe['Steps'].append(stripped_line)
            else:
                current_recipe['RecipeName'] = stripped_line
        if current_recipe:
            recipes.append(current_recipe)

    for recipe in recipes:
        print(recipe['RecipeName'])
        print('Ingredients:', ', '.join(recipe['Ingredients']))
        print('Steps:')
        for step in recipe['Steps']:
            print(step)
        print()  

    while True:
        ingredient_query = input('Enter an ingredient to query (or type EXIT to terminate): ')
        if ingredient_query == 'EXIT':
            break
        found_recipes = [recipe['RecipeName'] for recipe in recipes if ingredient_query in recipe['Ingredients']]
        if found_recipes:
            print(f'The ingredient "{ingredient_query}" is found in the following recipes: {', '.join(found_recipes)}')
        else:
            print(f'The ingredient "{ingredient_query}" is not found in any recipe.')