def parse_recipe_ingredients(file_path):
    recipe_dict = {}
    with open(file_path, 'r') as file:
        content = file.read().strip().split('\n\n')

    for block in content:
        lines = block.strip().split('\n')
        if lines:
            recipe_name = lines[0].replace('Recipe: ', '').strip()
            ingredients = [line.replace('-', '').strip() for line in lines[2:]]
            recipe_dict[recipe_name] = ingredients

    return recipe_dict