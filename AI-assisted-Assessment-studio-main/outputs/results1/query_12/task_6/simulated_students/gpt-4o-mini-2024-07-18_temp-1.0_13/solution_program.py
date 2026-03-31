def organize_recipes(input_file):
    favorite_file = 'favorite_recipes.txt'
    to_try_file = 'to_try_recipes.txt'
    disliked_file = 'disliked_recipes.txt'

    with open(input_file, 'r') as infile:
        recipes = infile.readlines()

    favorite_recipes = []
    to_try_recipes = []
    disliked_recipes = []

    for recipe in recipes:
        recipe = recipe.strip()
        while True:
            response = input(f'How would you categorize the recipe "{recipe}"? (Favorite, To Try, Disliked): ')
            if response == 'Favorite':
                favorite_recipes.append(recipe)
                break
            elif response == 'To Try':
                to_try_recipes.append(recipe)
                break
            elif response == 'Disliked':
                disliked_recipes.append(recipe)
                break
            else:
                print('Invalid input. Please input again.')

    with open(favorite_file, 'w') as f:
        for recipe in favorite_recipes:
            f.write(recipe + '\n')

    with open(to_try_file, 'w') as f:
        for recipe in to_try_recipes:
            f.write(recipe + '\n')

    with open(disliked_file, 'w') as f:
        for recipe in disliked_recipes:
            f.write(recipe + '\n')
