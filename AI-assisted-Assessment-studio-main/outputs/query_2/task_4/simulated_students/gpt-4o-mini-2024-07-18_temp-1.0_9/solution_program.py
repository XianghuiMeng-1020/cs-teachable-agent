def organize_recipes(file_path):
    recipes = []
    with open(file_path, 'r') as file:
        content = file.read()

    recipe_blocks = content.split('/****')
    for block in recipe_blocks:
        if 'NAME' in block:
            lines = block.split('\n')
            for line in lines:
                if line.strip().startswith('NAME'):
                    name_index = lines.index(line) + 1
                    recipe_name = lines[name_index].strip()
                    recipes.append(recipe_name)

    return sorted(recipes)