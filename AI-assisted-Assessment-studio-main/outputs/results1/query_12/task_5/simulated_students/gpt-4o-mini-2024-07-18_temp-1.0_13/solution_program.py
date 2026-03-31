def recipe_manager(filename):
    with open(filename, 'r') as file:
        content = file.read()

    recipes = content.strip().split('\n\n')
    recipe_details = []

    for recipe in recipes:
        lines = recipe.strip().split('\n')
        recipe_name = lines[0]
        ingredients_line = lines[1]
        ingredients = ingredients_line.split(': ')[1].split(', ')
        recipe_details.append((recipe_name, ingredients))
        print(f'Recipe Name: {recipe_name}')
        print(f'Ingredients: {ingredients_line}')
        print('Steps:')
        for step in lines[2:]:
            print(step)
        print()  

    while True:
        ingredient_query = input('Enter an ingredient to search (or type EXIT to quit): ')
        if ingredient_query == 'EXIT':
            break
        found_recipes = [recipe_name for recipe_name, ingredients in recipe_details if ingredient_query in ingredients]
        if found_recipes:
            print(f'Ingredient found in recipes: {', '.join(found_recipes)}')
        else:
            print('Ingredient not found in any recipe.')