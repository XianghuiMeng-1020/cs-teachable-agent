def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    recipes = []
    blocks = content.split('/****')
    for block in blocks:
        if 'NAME' in block:
            lines = block.split('\n')
            name_line = [line for line in lines if 'NAME' in line]
            if name_line:
                name_index = lines.index(name_line[0]) + 1
                if name_index < len(lines):
                    recipe_name = lines[name_index].strip()
                    if recipe_name:
                        recipes.append(recipe_name)

    return sorted(recipes)