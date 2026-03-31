def parse_recipe_ingredients(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = {}
    recipe_name = None
    ingredients = []
    lines = content.splitlines()

    for line in lines:
        if line.startswith('Recipe:'):
            if recipe_name:
                recipes[recipe_name] = ingredients
            recipe_name = line.split(': ')[1]
            ingredients = []
        elif line.startswith('-'):
            ingredients.append(line[2:])

    if recipe_name:
        recipes[recipe_name] = ingredients

    return recipes