def organize_recipes(file_path):
    recipes = []
    with open(file_path, 'r') as file:
        content = file.read()
        blocks = content.split('/****')
        for block in blocks:
            if 'NAME' in block:
                lines = block.split('\n')
                for line in lines:
                    if 'NAME' in line:
                        name_line_index = lines.index(line) + 1
                        recipe_name = lines[name_line_index].strip()
                        recipes.append(recipe_name)
    return sorted(recipes)