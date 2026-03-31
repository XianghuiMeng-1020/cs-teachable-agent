def parse_recipe_ingredients(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    recipes = {}
    current_recipe = None

    for line in lines:
        line = line.strip()
        if line.startswith('Recipe:'):
            if current_recipe is not None:
                recipes[current_recipe] = ingredients
            current_recipe = line[len('Recipe: '):].strip()
            ingredients = []
        elif line.startswith('Ingredients:'):
            continue
        else:
            ingredients.append(line)

    if current_recipe is not None:
        recipes[current_recipe] = ingredients

    return recipes