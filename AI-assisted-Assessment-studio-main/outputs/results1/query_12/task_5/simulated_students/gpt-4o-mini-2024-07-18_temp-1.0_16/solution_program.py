def recipe_manager(filename):
    with open(filename, 'r') as file:
        recipes = file.read().strip().split('\n\n')
    recipe_list = []

    for recipe in recipes:
        recipe_lines = recipe.strip().split('\n')
        recipe_name = recipe_lines[0].strip()
        ingredients_line = recipe_lines[1].strip()
        ingredients = ingredients_line.split(': ')[1].split(', ')
        steps = '\n'.join(recipe_lines[2:]).strip()
        recipe_list.append((recipe_name, ingredients, steps))

    for recipe_name, ingredients, steps in recipe_list:
        print(f'Recipe: {recipe_name}')
        print(f'Ingredients: {ingredients}')
        print(f'Steps:
{steps}\n')

    while True:
        ingredient_query = input('Enter an ingredient to search or type "EXIT" to quit: ')
        if ingredient_query == "EXIT":
            break
        found_in = []
        for recipe_name, ingredients, _ in recipe_list:
            if ingredient_query in ingredients:
                found_in.append(recipe_name)
        if found_in:
            print(f'The ingredient "{ingredient_query}" is found in: {', '.join(found_in)}')
        else:
            print(f'The ingredient "{ingredient_query}" is not found in any recipe.')