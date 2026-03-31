def organize_recipes(input_file):
    with open(input_file, 'r') as f:
        recipes = f.readlines()

    favorites = []
    to_try = []
    disliked = []

    for recipe in recipes:
        recipe = recipe.strip()
        while True:
            user_input = input(f'Categorize recipe "{recipe}": ')
            if user_input == 'Favorite':
                favorites.append(recipe)
                break
            elif user_input == 'To Try':
                to_try.append(recipe)
                break
            elif user_input == 'Disliked':
                disliked.append(recipe)
                break
            else:
                print('Invalid input. Please input again.')

    with open('favorite_recipes.txt', 'w') as f:
        for item in favorites:
            f.write(item + '\n')

    with open('to_try_recipes.txt', 'w') as f:
        for item in to_try:
            f.write(item + '\n')

    with open('disliked_recipes.txt', 'w') as f:
        for item in disliked:
            f.write(item + '\n')