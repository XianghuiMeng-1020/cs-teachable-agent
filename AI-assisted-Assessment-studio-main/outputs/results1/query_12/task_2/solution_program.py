def read_vegetarian_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    recipes = content.strip().split('\n\n')
    vegetarian_recipes = []
    for recipe in recipes:
        lines = recipe.split('\n')
        if len(lines) > 1:
            ingredients = lines[1].lower()
            if not any(meat in ingredients for meat in ['chicken', 'beef', 'pork', 'fish']):
                vegetarian_recipes.append(recipe)
    with open('vegetarian_recipes.txt', 'w') as veg_file:
        for veg_recipe in vegetarian_recipes:
            veg_file.write(veg_recipe + '\n\n')
