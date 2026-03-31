def parse_recipe_ingredients(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = {}
    current_recipe = None
    ingredients = []

    for line in content.splitlines():
        line = line.strip()  # remove any leading or trailing whitespace
        if line.startswith('Recipe:'):
            # If there's an active recipe, save its ingredients
            if current_recipe:
                recipes[current_recipe] = ingredients
            # Start a new recipe
            current_recipe = line[len('Recipe:'):].strip()
            ingredients = []
        elif line.startswith('-'):
            ingredients.append(line[1:].strip())

    # Add the last recipe and its ingredients
    if current_recipe:
        recipes[current_recipe] = ingredients

    return recipes