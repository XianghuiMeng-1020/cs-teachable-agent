def organize_recipes(input_file):
    favorites = []
    to_try = []
    disliked = []
    with open(input_file, 'r') as file:
        recipes = file.readlines()
    for recipe in recipes:
        recipe = recipe.strip()
        while True:
            response = input(f'Categorize the recipe "{recipe}": ').strip()
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
                print('Please input either "Favorite", "To Try", or "Disliked".')
    with open('favorite_recipes.txt', 'w') as f:
        f.write('\n'.join(favorites))
    with open('to_try_recipes.txt', 'w') as f:
        f.write('\n'.join(to_try))
    with open('disliked_recipes.txt', 'w') as f:
        f.write('\n'.join(disliked))