def parse_recipe_ingredients(file_path):
    recipes = {}
    with open(file_path, 'r') as file:
        current_recipe = None
        for line in file:
            line = line.strip()
            if line.startswith('Recipe:'):
                current_recipe = line[8:]
                recipes[current_recipe] = []
            elif line.startswith('-') and current_recipe is not None:
                recipes[current_recipe].append(line[2:])
    return recipes