def find_recipes_with_ingredient(file_path, ingredient):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = content.strip().split('

')
    recipe_names = []

    for recipe in recipes:
        lines = recipe.strip().split('
')
        recipe_name = lines[0]
        ingredients = lines[1:]
        if ingredient in ingredients:
            recipe_names.append(recipe_name)

    return recipe_names