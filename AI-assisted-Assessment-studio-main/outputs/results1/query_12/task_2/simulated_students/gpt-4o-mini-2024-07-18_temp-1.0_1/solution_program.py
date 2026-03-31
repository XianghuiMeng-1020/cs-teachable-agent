def read_vegetarian_recipes(file_path):
    with open(file_path, 'r') as file:
        recipes = file.read().strip().split('\n\n')

    vegetarian_recipes = []
    non_vegetarian_terms = ['chicken', 'beef', 'pork', 'fish']

    for recipe in recipes:
        if not any(term in recipe.lower() for term in non_vegetarian_terms):
            vegetarian_recipes.append(recipe)

    with open('vegetarian_recipes.txt', 'w') as output_file:
        output_file.write('\n\n'.join(vegetarian_recipes))