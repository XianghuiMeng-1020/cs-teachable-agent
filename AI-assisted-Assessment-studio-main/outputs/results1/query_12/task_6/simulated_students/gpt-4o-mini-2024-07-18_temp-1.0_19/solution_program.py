def organize_recipes(input_file):
    favorite_recipes = []
    to_try_recipes = []
    disliked_recipes = []
    with open(input_file, 'r') as file:
        recipes = file.readlines()
    for recipe in recipes:
        recipe = recipe.strip()
        while True:
            user_input = input(f"How would you categorize the recipe '{recipe}'? (Favorite, To Try, Disliked): ").strip()
            if user_input == 'Favorite':
                favorite_recipes.append(recipe)
                break
            elif user_input == 'To Try':
                to_try_recipes.append(recipe)
                break
            elif user_input == 'Disliked':
                disliked_recipes.append(recipe)
                break
            else:
                print("Invalid input. Please enter either 'Favorite', 'To Try', or 'Disliked'.")
    with open('favorite_recipes.txt', 'w') as fav_file:
        fav_file.write('\n'.join(favorite_recipes))
    with open('to_try_recipes.txt', 'w') as try_file:
        try_file.write('\n'.join(to_try_recipes))
    with open('disliked_recipes.txt', 'w') as dis_file:
        dis_file.write('\n'.join(disliked_recipes))