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
                current_recipe = line[8:]  # Get the recipe name
                current_ingredients = []
            elif line.startswith('-'):
                ingredient = line[2:].strip()  # Get the ingredient, skip '- '
                current_ingredients.append(ingredient)

        if current_recipe:
            recipes[current_recipe] = current_ingredients  # Add the last recipe

    return recipes