def read_vegetarian_recipes(file_path):
    non_veg_keywords = ['chicken', 'beef', 'pork', 'fish']
    vegetarian_recipes = []
    with open(file_path, 'r') as file:
        recipes = file.read().strip().split('\n\n')
        for recipe in recipes:
            if not any(keyword in recipe.lower() for keyword in non_veg_keywords):
                vegetarian_recipes.append(recipe)
    with open('vegetarian_recipes.txt', 'w') as output_file:
        output_file.write('\n\n'.join(vegetarian_recipes))