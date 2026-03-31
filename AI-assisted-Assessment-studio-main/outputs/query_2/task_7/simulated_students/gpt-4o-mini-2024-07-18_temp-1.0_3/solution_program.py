def parse_recipe_ingredients(file_path):
    recipes = {}
    current_recipe = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Recipe:'):
                current_recipe = line[len('Recipe:'):].strip()
                recipes[current_recipe] = []
            elif line.startswith('-') and current_recipe:
                ingredient = line[1:].strip()
                recipes[current_recipe].append(ingredient)
    return recipes