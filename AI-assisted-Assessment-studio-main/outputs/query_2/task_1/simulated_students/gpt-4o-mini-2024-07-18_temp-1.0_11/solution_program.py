def find_recipes_with_ingredient(file_path, ingredient):
    with open(file_path, 'r') as file:
        content = file.read().strip()  

    recipes = content.split('\n\n')
    recipe_names = []

    for recipe in recipes:
        lines = recipe.split('\n')
        recipe_name = lines[0].strip()
        ingredients = [line.strip() for line in lines[1:] if line.strip()]  

        if ingredient in ingredients:
            recipe_names.append(recipe_name)

    return recipe_names