def organize_recipes(input_file):
    favorites = []
    to_try = []
    disliked = []
    with open(input_file, 'r') as file:
        recipes = file.readlines()
        for recipe in recipes:
            recipe_name = recipe.strip()
            while True:
                category = input(f"How do you categorize '{recipe_name}'? (Favorite, To Try, Disliked): ").strip()
                if category == 'Favorite':
                    favorites.append(recipe_name)
                    break
                elif category == 'To Try':
                    to_try.append(recipe_name)
                    break
                elif category == 'Disliked':
                    disliked.append(recipe_name)
                    break
                else:
                    print("Invalid input, please enter 'Favorite', 'To Try', or 'Disliked'.")
    with open('favorite_recipes.txt', 'w') as file:
        for recipe in favorites:
            file.write(recipe + "\n")
    with open('to_try_recipes.txt', 'w') as file:
        for recipe in to_try:
            file.write(recipe + "\n")
    with open('disliked_recipes.txt', 'w') as file:
        for recipe in disliked:
            file.write(recipe + "\n")