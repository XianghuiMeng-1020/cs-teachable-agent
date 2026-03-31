def organize_recipes(input_file):
    favorite_recipes = []
    to_try_recipes = []
    disliked_recipes = []
    
    with open(input_file, 'r') as file:
        recipes = file.readlines()
    
    for recipe in recipes:
        recipe = recipe.strip()
        while True:
            user_input = input(f'How would you categorize the recipe "{recipe}"? (Favorite/To Try/Disliked): ')
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
                print('Invalid input. Please enter "Favorite", "To Try", or "Disliked".')
    
    with open('favorite_recipes.txt', 'w') as f:
        for recipe in favorite_recipes:
            f.write(recipe + '\n')
    
    with open('to_try_recipes.txt', 'w') as f:
        for recipe in to_try_recipes:
            f.write(recipe + '\n')
    
    with open('disliked_recipes.txt', 'w') as f:
        for recipe in disliked_recipes:
            f.write(recipe + '\n')