def parse_recipe_ingredients(file_path):
    recipes = {}
    current_recipe = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Recipe:'):
                if current_recipe is not None:
                    recipes[current_recipe] = ingredients
                current_recipe = line[len('Recipe: '):]
                ingredients = []
            elif line.startswith('Ingredients:'):
                continue
            elif line:
                ingredients.append(line[2:])  # skip the '- '

        if current_recipe is not None:
            recipes[current_recipe] = ingredients

    return recipes