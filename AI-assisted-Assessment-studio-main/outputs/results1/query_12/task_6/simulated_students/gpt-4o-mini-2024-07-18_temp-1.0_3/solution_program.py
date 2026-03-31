def organize_recipes(input_file):
    with open(input_file, 'r') as file:
        recipes = file.readlines()

    for recipe in recipes:
        recipe = recipe.strip()
        while True:
            category = input(f'How would you categorize the recipe "{recipe}"? (Favorite, To Try, Disliked): ')
            if category == 'Favorite':
                with open('favorite_recipes.txt', 'a') as fav_file:
                    fav_file.write(recipe + '\n')
                break
            elif category == 'To Try':
                with open('to_try_recipes.txt', 'a') as try_file:
                    try_file.write(recipe + '\n')
                break
            elif category == 'Disliked':
                with open('disliked_recipes.txt', 'a') as disliked_file:
                    disliked_file.write(recipe + '\n')
                break
            else:
                print('Invalid input. Please enter Favorite, To Try, or Disliked.')