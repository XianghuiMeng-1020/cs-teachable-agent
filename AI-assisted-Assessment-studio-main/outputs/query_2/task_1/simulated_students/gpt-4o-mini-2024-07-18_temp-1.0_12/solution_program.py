def find_recipes_with_ingredient(file_path, ingredient):
    recipes_with_ingredient = []
    with open(file_path, 'r') as file:
        content = file.read().strip()
    recipes = content.split('\n\n')
    for recipe in recipes:
        lines = recipe.split('\n')
        recipe_name = lines[0].strip()
        ingredients = [line.strip() for line in lines[1:]]
        if ingredient in ingredients:
            recipes_with_ingredient.append(recipe_name)
    return recipes_with_ingredient