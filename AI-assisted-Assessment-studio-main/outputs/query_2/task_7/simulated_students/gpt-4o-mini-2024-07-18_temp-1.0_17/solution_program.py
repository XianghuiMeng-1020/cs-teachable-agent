def parse_recipe_ingredients(file_path):
    recipes = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_recipe = None
        ingredients = []
        for line in lines:
            line = line.strip()
            if line.startswith('Recipe:'):
                if current_recipe is not None:
                    recipes[current_recipe] = ingredients
                current_recipe = line[len('Recipe: '):]
                ingredients = []
            elif line.startswith('Ingredients:'):
                continue
            elif line:
                ingredients.append(line[2:])
        if current_recipe is not None:
            recipes[current_recipe] = ingredients
    return recipes