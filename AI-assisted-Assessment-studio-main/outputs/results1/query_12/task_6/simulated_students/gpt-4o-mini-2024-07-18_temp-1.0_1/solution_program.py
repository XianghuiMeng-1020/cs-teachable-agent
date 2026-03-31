def organize_recipes(input_file):
    with open(input_file, 'r') as file:
        recipes = file.readlines()

    for recipe in recipes:
        recipe = recipe.strip()
        while True:
            response = input(f"How would you categorize the recipe '{recipe}'? (Favorite, To Try, Disliked): ")
            if response == 'Favorite':
                with open('favorite_recipes.txt', 'a') as favorite_file:
                    favorite_file.write(recipe + '\n')
                break
            elif response == 'To Try':
                with open('to_try_recipes.txt', 'a') as to_try_file:
                    to_try_file.write(recipe + '\n')
                break
            elif response == 'Disliked':
                with open('disliked_recipes.txt', 'a') as disliked_file:
                    disliked_file.write(recipe + '\n')
                break
            else:
                print("Invalid input. Please enter 'Favorite', 'To Try', or 'Disliked'.")