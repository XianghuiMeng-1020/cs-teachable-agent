def organize_recipes(input_file):
    favorite_file = 'favorite_recipes.txt'
    to_try_file = 'to_try_recipes.txt'
    disliked_file = 'disliked_recipes.txt'

    with open(input_file, 'r') as file:
        recipes = file.readlines()

    for recipe in recipes:
        recipe = recipe.strip()
        response = input(f"How do you categorize the recipe '{recipe}'? (Favorite, To Try, Disliked): ").strip()
        while response not in ['Favorite', 'To Try', 'Disliked']:
            response = input("Invalid input. Please enter 'Favorite', 'To Try', or 'Disliked': ").strip()

        if response == 'Favorite':
            with open(favorite_file, 'a') as f:
                f.write(recipe + '\n')
        elif response == 'To Try':
            with open(to_try_file, 'a') as f:
                f.write(recipe + '\n')
        elif response == 'Disliked':
            with open(disliked_file, 'a') as f:
                f.write(recipe + '\n')
