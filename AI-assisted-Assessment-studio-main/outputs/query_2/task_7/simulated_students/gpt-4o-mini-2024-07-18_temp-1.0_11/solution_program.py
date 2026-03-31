def parse_recipe_ingredients(file_path):
    recipes = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_recipe = None
        ingredients_list = []
        for line in lines:
            line = line.strip()
            if line.startswith('Recipe:'):
                if current_recipe is not None:
                    recipes[current_recipe] = ingredients_list
                current_recipe = line.replace('Recipe: ', '')
                ingredients_list = []
            elif line.startswith('Ingredients:'):
                continue
            elif line.startswith('-'):
                ingredients_list.append(line[2:])
        if current_recipe is not None:
            recipes[current_recipe] = ingredients_list
    return recipes