def parse_recipe_ingredients(file_path):
    recipes = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        recipe_name = None
        ingredients = []
        for line in lines:
            line = line.strip()
            if line.startswith('Recipe:'):
                if recipe_name is not None:
                    recipes[recipe_name] = ingredients
                recipe_name = line.split(': ')[1]
                ingredients = []
            elif line.startswith('Ingredients:'):
                continue
            elif line.startswith('-'):
                ingredients.append(line[2:])
        if recipe_name is not None:
            recipes[recipe_name] = ingredients
    return recipes