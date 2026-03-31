def find_recipes_with_ingredient(file_path, ingredient):
    with open(file_path, 'r') as file:
        content = file.read().strip().split('\n\n')
    recipes_with_ingredient = []
    for recipe in content:
        lines = recipe.split('\n')
        recipe_name = lines[0]  
        ingredients = lines[1:]  
        if ingredient in ingredients:
            recipes_with_ingredient.append(recipe_name)
    return recipes_with_ingredient