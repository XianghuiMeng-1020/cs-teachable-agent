def parse_recipe_ingredients(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    recipes = content.strip().split('\n\n')
    recipe_dict = {}
    for recipe in recipes:
        lines = recipe.split('\n')
        recipe_name = lines[0].split(': ')[1]
        ingredients = [line.strip('- ').strip() for line in lines[1:] if line.startswith('-')]
        recipe_dict[recipe_name] = ingredients
    return recipe_dict