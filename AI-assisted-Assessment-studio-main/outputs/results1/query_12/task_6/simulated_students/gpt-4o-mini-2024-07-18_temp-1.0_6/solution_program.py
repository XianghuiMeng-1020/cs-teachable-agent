def organize_recipes(input_file):
    with open(input_file, 'r') as infile:
        recipes = infile.readlines()
    favorite_recipes = []
    to_try_recipes = []
    disliked_recipes = []
    for recipe in recipes:
        recipe = recipe.strip()
        while True:
            category = input(f'Categorize the recipe "{recipe}": ')
            if category == 'Favorite':
                favorite_recipes.append(recipe)
                break
            elif category == 'To Try':
                to_try_recipes.append(recipe)
                break
            elif category == 'Disliked':
                disliked_recipes.append(recipe)
                break
            else:
                print('Invalid input. Please enter Favorite, To Try, or Disliked.')
    with open('favorite_recipes.txt', 'w') as f:
        for item in favorite_recipes:
            f.write(f'{item}\n')
    with open('to_try_recipes.txt', 'w') as f:
        for item in to_try_recipes:
            f.write(f'{item}\n')
    with open('disliked_recipes.txt', 'w') as f:
        for item in disliked_recipes:
            f.write(f'{item}\n')