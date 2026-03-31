def parse_recipe_ingredients(file_path):
    recipes = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_recipe = None
        current_ingredients = []
        for line in lines:
            line = line.strip()
            if line.startswith('Recipe:'):
                if current_recipe is not None:
                    recipes[current_recipe] = current_ingredients
                current_recipe = line[len('Recipe: '):].strip()
                current_ingredients = []
            elif line.startswith('Ingredients:'):
                continue
            elif line.startswith('-'):
                ingredient = line[1:].strip()
                current_ingredients.append(ingredient)
        if current_recipe is not None:
            recipes[current_recipe] = current_ingredients
    return recipes