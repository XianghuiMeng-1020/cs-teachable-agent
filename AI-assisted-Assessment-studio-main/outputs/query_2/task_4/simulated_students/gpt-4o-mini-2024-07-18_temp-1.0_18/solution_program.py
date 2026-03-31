def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = []
    blocks = content.split('/****')

    for block in blocks:
        if 'NAME' in block:
            lines = block.split('\n')
            for line in lines:
                if 'NAME' in line:
                    recipe_name = line.split('\n')[1].strip()
                    recipes.append(recipe_name)

    sorted_recipes = sorted(recipes)
    return sorted_recipes