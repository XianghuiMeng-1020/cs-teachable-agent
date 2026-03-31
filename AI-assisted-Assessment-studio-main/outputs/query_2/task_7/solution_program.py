def parse_recipe_ingredients(file_path):
    recipes = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    current_recipe = None
    current_ingredients = []
    for line in lines:
        line = line.strip()
        if line.startswith('Recipe:'):
            if current_recipe:
                recipes[current_recipe] = current_ingredients
            current_recipe = line.split(': ')[1]
            current_ingredients = []
        elif line.startswith('-'):
            current_ingredients.append(line[2:].strip())
    if current_recipe:
        recipes[current_recipe] = current_ingredients
    return recipes
