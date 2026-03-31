def organize_recipes(input_file):
    with open(input_file, 'r') as f:
        recipes = f.readlines()

    favorite_recipes = []
    to_try_recipes = []
    disliked_recipes = []

    for recipe in recipes:
        recipe = recipe.strip()
        user_input = input(f'How would you categorize the recipe "{recipe}"? (Favorite, To Try, Disliked): ')
        while user_input not in ['Favorite', 'To Try', 'Disliked']:
            user_input = input('Invalid input. Please categorize the recipe again (Favorite, To Try, Disliked): ')

        if user_input == 'Favorite':
            favorite_recipes.append(recipe)
        elif user_input == 'To Try':
            to_try_recipes.append(recipe)
        elif user_input == 'Disliked':
            disliked_recipes.append(recipe)

    with open('favorite_recipes.txt', 'w') as f:
        for recipe in favorite_recipes:
            f.write(recipe + '\n')

    with open('to_try_recipes.txt', 'w') as f:
        for recipe in to_try_recipes:
            f.write(recipe + '\n')

    with open('disliked_recipes.txt', 'w') as f:
        for recipe in disliked_recipes:
            f.write(recipe + '\n')
