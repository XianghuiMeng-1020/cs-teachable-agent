def read_vegetarian_recipes(file_path):
    non_vegetarian_keywords = ['chicken', 'beef', 'pork', 'fish']
    vegetarian_recipes = []
    with open(file_path, 'r') as file:
        content = file.read()
        recipes = content.split('\n\n')
        for recipe in recipes:
            if any(keyword in recipe.lower() for keyword in non_vegetarian_keywords):
                continue
            vegetarian_recipes.append(recipe.strip())
    with open('vegetarian_recipes.txt', 'w') as output_file:
        output_file.write('\n\n'.join(vegetarian_recipes))