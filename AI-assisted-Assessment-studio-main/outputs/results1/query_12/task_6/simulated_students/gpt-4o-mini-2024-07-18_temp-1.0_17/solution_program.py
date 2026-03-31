def organize_recipes(input_file):
    favorites = []
    to_try = []
    disliked = []
    
    with open(input_file, 'r') as file:
        recipes = file.readlines()
    
    for recipe in recipes:
        recipe = recipe.strip()
        while True:
            response = input(f'How would you categorize the recipe "{recipe}"? (Favorite, To Try, Disliked): ')
            if response == 'Favorite':
                favorites.append(recipe)
                break
            elif response == 'To Try':
                to_try.append(recipe)
                break
            elif response == 'Disliked':
                disliked.append(recipe)
                break
            else:
                print('Invalid input. Please enter Favorite, To Try, or Disliked.')
                
    with open('favorite_recipes.txt', 'w') as fav_file:
        for item in favorites:
            fav_file.write(item + '\n')

    with open('to_try_recipes.txt', 'w') as try_file:
        for item in to_try:
            try_file.write(item + '\n')

    with open('disliked_recipes.txt', 'w') as dis_file:
        for item in disliked:
            dis_file.write(item + '\n')