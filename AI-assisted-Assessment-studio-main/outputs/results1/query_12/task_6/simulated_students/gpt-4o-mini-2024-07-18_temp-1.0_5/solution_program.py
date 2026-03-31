def organize_recipes(input_file):
    with open(input_file, 'r') as infile:
        recipes = infile.readlines()

    for recipe in recipes:
        recipe = recipe.strip()
        while True:
            user_input = input(f"How would you categorize the recipe '{recipe}'? (Favorite, To Try, Disliked): ").strip()
            if user_input == 'Favorite':
                with open('favorite_recipes.txt', 'a') as fav_file:
                    fav_file.write(recipe + '\n')
                break
            elif user_input == 'To Try':
                with open('to_try_recipes.txt', 'a') as try_file:
                    try_file.write(recipe + '\n')
                break
            elif user_input == 'Disliked':
                with open('disliked_recipes.txt', 'a') as dislike_file:
                    dislike_file.write(recipe + '\n')
                break
            else:
                print('Invalid input. Please enter Favorite, To Try, or Disliked.')
