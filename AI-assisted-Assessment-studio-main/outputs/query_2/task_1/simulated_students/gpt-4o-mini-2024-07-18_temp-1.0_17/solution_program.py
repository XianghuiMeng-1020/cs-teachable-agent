def find_recipes_with_ingredient(file_path, ingredient):
    recipes = []
    current_recipe = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line == '':
                if current_recipe:
                    recipes.append(current_recipe)
                    current_recipe = None
            elif current_recipe is None:
                current_recipe = {'name': line, 'ingredients': []}
            else:
                current_recipe['ingredients'].append(line)
        if current_recipe:
            recipes.append(current_recipe)

    result = []
    for recipe in recipes:
        if ingredient in recipe['ingredients']:
            result.append(recipe['name'])

    return result