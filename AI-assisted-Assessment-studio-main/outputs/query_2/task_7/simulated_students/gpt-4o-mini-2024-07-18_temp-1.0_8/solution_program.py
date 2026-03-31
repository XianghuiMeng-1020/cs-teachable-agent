def parse_recipe_ingredients(file_path):
    recipes = {}
    current_recipe = None
    ingredients = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Recipe:'):
                if current_recipe:
                    recipes[current_recipe] = ingredients
                current_recipe = line.split(': ')[1]
                ingredients = []
            elif line.startswith('Ingredients:'):
                continue
            elif line:
                ingredients.append(line[2:])

        if current_recipe:
            recipes[current_recipe] = ingredients

    return recipes