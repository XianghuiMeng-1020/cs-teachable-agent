def find_recipes_with_ingredient(file_path, ingredient):
    with open(file_path, 'r') as file:
        content = file.read().strip()

    recipes = content.split('\n\n')
    matching_recipes = []

    for recipe in recipes:
        lines = recipe.split('\n')
        recipe_name = lines[0].strip()
        ingredients = set(line.strip() for line in lines[1:] if line.strip())
        if ingredient in ingredients:
            matching_recipes.append(recipe_name)

    return matching_recipes