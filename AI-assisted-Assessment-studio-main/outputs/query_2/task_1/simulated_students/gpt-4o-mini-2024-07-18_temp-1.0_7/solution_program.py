def find_recipes_with_ingredient(file_path, ingredient):
    recipes_with_ingredient = []
    recipe_name = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line == '':
                recipe_name = None
                continue
            if recipe_name is None:
                recipe_name = line
                ingredients = []
            else:
                ingredients.append(line)
                if ingredient in ingredients:
                    recipes_with_ingredient.append(recipe_name)
                    recipe_name = None  # reset for the next recipe
    return recipes_with_ingredient