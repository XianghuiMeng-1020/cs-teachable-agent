def recipe_manager(filename):
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n\n')
        recipes = []
        ingredient_recipes = {}

        for recipe_block in content:
            lines = recipe_block.strip().split('\n')
            if len(lines) < 3:
                continue
            recipe_name = lines[0].strip()
            ingredients_line = lines[1].strip()
            ingredients = ingredients_line.replace('Ingredients: ', '').split(', ')
            steps = lines[2:]
            recipes.append((recipe_name, ingredients, steps))
            for ingredient in ingredients:
                if ingredient in ingredient_recipes:
                    ingredient_recipes[ingredient].append(recipe_name)
                else:
                    ingredient_recipes[ingredient] = [recipe_name]

        for recipe in recipes:
            print(recipe[0])  # Display recipe name
            print('Ingredients:', ', '.join(recipe[1]))
            print('Steps:')
            for step in recipe[2]:
                print(step)
            print()  # Separate recipes with a newline

        while True:
            query = input('Enter an ingredient to search (or type EXIT to quit): ').strip()
            if query == 'EXIT':
                break
            if query in ingredient_recipes:
                print(f'Recipes containing {query}: {", ".join(ingredient_recipes[query])}')
            else:
                print(f'{query} not found in any recipes.')