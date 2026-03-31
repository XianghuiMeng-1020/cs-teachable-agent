def find_recipes_with_ingredient(file_path, ingredient):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = content.strip().split('\n\n')
    matching_recipes = []

    for recipe in recipes:
        lines = recipe.strip().split('\n')
        recipe_name = lines[0]
        ingredients = lines[1:]
        if ingredient in ingredients:
            matching_recipes.append(recipe_name)

    return matching_recipes