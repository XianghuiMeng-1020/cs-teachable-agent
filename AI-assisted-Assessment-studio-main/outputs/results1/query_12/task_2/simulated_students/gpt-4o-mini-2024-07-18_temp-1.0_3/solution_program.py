def read_vegetarian_recipes(file_path):
    non_veg_words = ['chicken', 'beef', 'pork', 'fish']
    vegetarian_recipes = []

    with open(file_path, 'r') as file:
        content = file.read()
        recipes = content.split('\n\n')

        for recipe in recipes:
            if not any(word in recipe.lower() for word in non_veg_words):
                vegetarian_recipes.append(recipe.strip())

    with open('vegetarian_recipes.txt', 'w') as output_file:
        output_file.write('\n\n'.join(vegetarian_recipes))