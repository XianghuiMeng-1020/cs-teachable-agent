def organize_recipes(input_file):
    favorite_file = 'favorite_recipes.txt'
    to_try_file = 'to_try_recipes.txt'
    disliked_file = 'disliked_recipes.txt'

    with open(input_file, 'r') as file:
        recipes = file.readlines()

    for recipe in recipes:
        recipe = recipe.strip()
        user_input = ''
        while user_input not in ['Favorite', 'To Try', 'Disliked']:
            user_input = input(f'How would you categorize the recipe "{recipe}"? (Favorite, To Try, Disliked): ')

        if user_input == 'Favorite':
            with open(favorite_file, 'a') as fav_file:
                fav_file.write(recipe + '\n')
        elif user_input == 'To Try':
            with open(to_try_file, 'a') as try_file:
                try_file.write(recipe + '\n')
        elif user_input == 'Disliked':
            with open(disliked_file, 'a') as dislike_file:
                dislike_file.write(recipe + '\n')