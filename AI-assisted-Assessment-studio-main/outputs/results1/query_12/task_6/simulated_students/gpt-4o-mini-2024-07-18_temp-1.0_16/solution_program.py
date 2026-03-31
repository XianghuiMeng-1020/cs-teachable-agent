def organize_recipes(input_file):
    favorite_file = 'favorite_recipes.txt'
    to_try_file = 'to_try_recipes.txt'
    disliked_file = 'disliked_recipes.txt'

    with open(input_file, 'r') as infile:
        recipes = infile.readlines()

    with open(favorite_file, 'w') as fav_file, open(to_try_file, 'w') as try_file, open(disliked_file, 'w') as dislike_file:
        for recipe in recipes:
            recipe = recipe.strip()
            while True:
                user_input = input(f"How would you categorize the recipe '{recipe}'? (Favorite, To Try, Disliked): ")
                if user_input == 'Favorite':
                    fav_file.write(recipe + '\n')
                    break
                elif user_input == 'To Try':
                    try_file.write(recipe + '\n')
                    break
                elif user_input == 'Disliked':
                    dislike_file.write(recipe + '\n')
                    break
                else:
                    print("Invalid input. Please enter 'Favorite', 'To Try', or 'Disliked'.")