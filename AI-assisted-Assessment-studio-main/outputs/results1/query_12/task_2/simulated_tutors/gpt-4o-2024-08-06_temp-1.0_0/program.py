def read_vegetarian_recipes(file_path):
    vegetarian_keywords = ['chicken', 'beef', 'pork', 'fish']
    with open(file_path, 'r') as file:
        recipes = file.read().strip().split('\n\n')
    
    vegetarian_recipes = []
    for recipe in recipes:
        recipe_lower = recipe.lower()
        if not any(keyword in recipe_lower for keyword in vegetarian_keywords):
            vegetarian_recipes.append(recipe)
    
    with open("vegetarian_recipes.txt", 'w') as file:
        file.write('\n\n'.join(vegetarian_recipes))