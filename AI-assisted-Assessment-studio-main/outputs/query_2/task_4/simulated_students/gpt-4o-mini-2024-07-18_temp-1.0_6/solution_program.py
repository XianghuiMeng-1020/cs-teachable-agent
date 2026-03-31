def organize_recipes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    recipes = []
    blocks = content.split('/*')
    for block in blocks:
        if 'NAME' in block and 'INGREDIENTS' in block:
            lines = block.split('\n')
            name_line = next((line for line in lines if 'NAME' in line), None)
            if name_line:
                name = name_line.split('\n')[1].strip()
                recipes.append(name)
    return sorted(recipes)