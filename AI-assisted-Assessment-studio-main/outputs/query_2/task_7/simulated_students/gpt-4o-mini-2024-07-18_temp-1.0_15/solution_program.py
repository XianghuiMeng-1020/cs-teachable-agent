def parse_recipe_ingredients(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    recipes = {}
    current_recipe = None
    current_ingredients = []

    for line in lines:
        line = line.strip()
        if line.startswith("Recipe:"):
            if current_recipe is not None:
                recipes[current_recipe] = current_ingredients
            current_recipe = line.split(": ")[1]
            current_ingredients = []
        elif line.startswith("- "):
            ingredient = line[2:].strip()
            current_ingredients.append(ingredient)

    if current_recipe is not None:
        recipes[current_recipe] = current_ingredients

    return recipes