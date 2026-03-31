def recipe_manager(filename):
    recipes = []
    with open(filename, 'r') as file:
        current_recipe = ''
        current_ingredients = ''
        current_steps = ''
        reading_steps = False
        
        for line in file:
            if line.strip() == '':
                if current_recipe:
                    recipes.append((current_recipe, current_ingredients, current_steps))
                    current_recipe = ''
                    current_ingredients = ''
                    current_steps = ''
                    reading_steps = False
                continue
            if not current_recipe:
                current_recipe = line.strip()
            elif line.startswith('Ingredients:'):
                current_ingredients = line.strip().replace('Ingredients: ', '')
            elif line.startswith('Steps:'):
                reading_steps = True
            elif reading_steps:
                current_steps += line

    if current_recipe:
        recipes.append((current_recipe, current_ingredients, current_steps))

    # Display all recipes
    for recipe, ingredients, steps in recipes:
        print(f'Recipe: {recipe}')
        print(f'Ingredients: {ingredients}')
        print(f'Steps: {steps}\n')

    while True:
        query = input('Enter an ingredient to search or type EXIT to quit: ')
        if query == 'EXIT':
            break
        found = False
        for recipe, ingredients, steps in recipes:
            if query in ingredients.split(', '):
                found = True
                print(f'{recipe} uses {query}.')
        if not found:
            print(f'{query} is not found in any recipe.')