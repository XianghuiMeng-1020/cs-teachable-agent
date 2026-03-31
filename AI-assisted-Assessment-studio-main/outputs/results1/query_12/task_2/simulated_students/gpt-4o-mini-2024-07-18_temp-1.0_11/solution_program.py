def read_vegetarian_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = content.split('\n\n')
    vegetarian_recipes = []
    non_veg_keywords = ['chicken', 'beef', 'pork', 'fish']

    for recipe in recipes:
        if not any(keyword in recipe.lower() for keyword in non_veg_keywords):
            vegetarian_recipes.append(recipe.strip())

    with open('vegetarian_recipes.txt', 'w') as output_file:
        output_file.write('\n\n'.join(vegetarian_recipes))